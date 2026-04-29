#!/usr/bin/env python3
"""Manage manga character image memory metadata."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_IMAGES = (
    "portrait-front.png",
    "full-body-front.png",
    "turnaround-sheet.png",
    "expression-sheet.png",
    "pose-sheet.png",
)

MEMORY_VERSION = 2
DEFAULT_ASSET_GROUP = "main-characters"
DEFAULT_CHARACTER_VERSION = "base"
VERSION_TYPES = ("base", "variant", "evolution")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "character"


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def memory_paths(memory_root: Path) -> dict[str, Path]:
    return {
        "root": memory_root,
        "assets": memory_root / "assets",
        "main_characters": memory_root / "assets" / DEFAULT_ASSET_GROUP,
        "pages": memory_root / "pages",
        "manifest": memory_root / "manifest.json",
    }


def init_memory(memory_root: Path, project: str | None) -> dict[str, Any]:
    paths = memory_paths(memory_root)
    paths["main_characters"].mkdir(parents=True, exist_ok=True)
    paths["pages"].mkdir(parents=True, exist_ok=True)
    manifest = read_json(
        paths["manifest"],
        {"version": MEMORY_VERSION, "project": project or "Manga Project", "assets": {}, "pages": []},
    )
    manifest["version"] = MEMORY_VERSION
    manifest["project"] = project or manifest.get("project") or "Manga Project"
    manifest.setdefault("assets", {})
    manifest.setdefault("pages", [])
    manifest["updated_at"] = now_iso()
    write_json(paths["manifest"], manifest)
    return manifest


def character_dir(memory_root: Path, name: str, group: str) -> Path:
    return memory_root / "assets" / slugify(group) / slugify(name)


def character_version_dir(memory_root: Path, name: str, group: str, version: str) -> Path:
    return character_dir(memory_root, name, group) / "versions" / slugify(version)


def image_status(folder: Path) -> dict[str, str]:
    return {image: "present" if (folder / image).exists() else "missing" for image in REQUIRED_IMAGES}


def base_character_manifest(
    name: str,
    description: str,
    identity_markers: list[str],
    group: str,
    folder: Path,
) -> dict[str, Any]:
    existing = read_json(folder / "manifest.json", {})
    return {
        "name": existing.get("name") or name,
        "slug": folder.name,
        "asset_group": slugify(group),
        "description": existing.get("description") or description,
        "identity_markers": existing.get("identity_markers") or identity_markers,
        "versions": existing.get("versions", {}),
        "notes": existing.get("notes", []),
        "created_at": existing.get("created_at") or now_iso(),
        "updated_at": now_iso(),
    }


def version_manifest(
    character: dict[str, Any],
    version: str,
    version_type: str,
    description: str,
    identity_markers: list[str],
    folder: Path,
) -> dict[str, Any]:
    existing = read_json(folder / "manifest.json", {})
    return {
        "name": character["name"],
        "character_slug": character["slug"],
        "asset_group": character["asset_group"],
        "version": slugify(version),
        "version_type": version_type,
        "description": description or existing.get("description") or character.get("description", ""),
        "identity_markers": identity_markers or existing.get("identity_markers") or character.get("identity_markers", []),
        "inherits_from": DEFAULT_CHARACTER_VERSION if version_type in {"variant", "evolution"} else None,
        "required_images": image_status(folder),
        "created_at": existing.get("created_at") or now_iso(),
        "updated_at": now_iso(),
    }


def memory_prompt(name: str, manifest: dict[str, Any]) -> str:
    markers = ", ".join(manifest.get("identity_markers", [])) or "define stable identity markers"
    description = manifest.get("description") or "describe this character version precisely"
    return "\n".join(
        [
            f"# Missing Img-Memory Prompts For {name}",
            "",
            "Generate the missing reference images before creating manga pages.",
            "",
            f"Asset group: {manifest['asset_group']}",
            f"Character: {name}",
            f"Version: {manifest['version']} ({manifest['version_type']})",
            f"Description: {description}",
            f"Identity markers: {markers}",
            "",
            "Use consistent manga character design, clean line art, no text, no watermark.",
            "Preserve the same face, hair silhouette, body proportions, costume, and accessories unless this version explicitly changes them.",
            "For evolutions, keep visible lineage markers from the base version while making the requested transformation obvious.",
            "",
            "Required images:",
            *[f"- {image}: {manifest['required_images'][image]}" for image in REQUIRED_IMAGES],
            "",
        ]
    )


def ensure_character(args: argparse.Namespace) -> dict[str, Any]:
    init_memory(args.memory_root, args.project)
    group = slugify(args.group)
    version = slugify(args.version)
    character_folder = character_dir(args.memory_root, args.name, group)
    version_folder = character_version_dir(args.memory_root, args.name, group, version)
    character_folder.mkdir(parents=True, exist_ok=True)
    version_folder.mkdir(parents=True, exist_ok=True)

    markers = split_csv(args.identity_markers)
    existing_version = read_json(version_folder / "manifest.json", {})
    version_type = (
        args.version_type
        or existing_version.get("version_type")
        or ("base" if version == DEFAULT_CHARACTER_VERSION else "variant")
    )
    character = base_character_manifest(args.name, args.description or "", markers, group, character_folder)
    version_data = version_manifest(
        character,
        version,
        version_type,
        args.version_description or args.description or "",
        markers,
        version_folder,
    )
    character["versions"][version] = {
        "version_type": version_type,
        "path": str(version_folder.relative_to(args.memory_root)),
        "description": version_data["description"],
        "updated_at": version_data["updated_at"],
    }
    character["updated_at"] = now_iso()

    write_json(character_folder / "manifest.json", character)
    write_json(version_folder / "manifest.json", version_data)
    (version_folder / "prompt-to-generate.md").write_text(memory_prompt(args.name, version_data), encoding="utf-8")
    update_root_character(args.memory_root, character)
    return {"character": character, "version": version_data}


def update_root_character(memory_root: Path, character: dict[str, Any]) -> None:
    paths = memory_paths(memory_root)
    root = read_json(paths["manifest"], {"version": MEMORY_VERSION, "project": "", "assets": {}, "pages": []})
    root["version"] = MEMORY_VERSION
    assets = root.setdefault("assets", {})
    group = assets.setdefault(character["asset_group"], {})
    group[character["slug"]] = {
        "name": character["name"],
        "description": character.get("description", ""),
        "versions": character.get("versions", {}),
        "updated_at": character["updated_at"],
    }
    root["updated_at"] = now_iso()
    write_json(paths["manifest"], root)


def register_image(args: argparse.Namespace) -> dict[str, Any]:
    source = args.image.resolve()
    if not source.exists():
        raise FileNotFoundError(f"Image does not exist: {source}")
    if args.kind not in REQUIRED_IMAGES:
        allowed = ", ".join(REQUIRED_IMAGES)
        raise ValueError(f"Unknown image kind '{args.kind}'. Expected one of: {allowed}")

    ensured = ensure_character(args)
    target = character_version_dir(args.memory_root, args.name, args.group, args.version) / args.kind
    shutil.copy2(source, target)

    version_data = ensured["version"]
    version_data["required_images"] = image_status(target.parent)
    version_data["updated_at"] = now_iso()
    write_json(target.parent / "manifest.json", version_data)

    character = ensured["character"]
    character["versions"][version_data["version"]]["updated_at"] = version_data["updated_at"]
    write_json(character_dir(args.memory_root, args.name, args.group) / "manifest.json", character)
    update_root_character(args.memory_root, character)
    return {"registered": str(target), "character": character, "version": version_data}


def missing_report(memory_root: Path, names: list[str], group: str, version: str) -> dict[str, Any]:
    report: dict[str, Any] = {
        "memory_root": str(memory_root),
        "asset_group": slugify(group),
        "version": slugify(version),
        "characters": {},
    }
    for name in names:
        folder = character_version_dir(memory_root, name, group, version)
        status = image_status(folder)
        report["characters"][slugify(name)] = {
            "name": name,
            "exists": folder.exists(),
            "path": str(folder),
            "missing": [image for image, value in status.items() if value == "missing"],
            "required_images": status,
        }
    return report


def record_page(args: argparse.Namespace) -> dict[str, Any]:
    init_memory(args.memory_root, args.project)
    page_id = args.page_id
    characters = [
        {
            "asset_group": slugify(args.group),
            "character": slugify(name),
            "version": slugify(args.version),
        }
        for name in split_csv(args.characters)
    ]
    payload = {
        "page_id": page_id,
        "characters": characters,
        "scene_state": args.scene_state or "",
        "output_image": str(args.output_image) if args.output_image else "",
        "memory_images_used": split_csv(args.memory_images_used),
        "created_at": now_iso(),
    }
    write_json(args.memory_root / "pages" / f"{page_id}.json", payload)
    update_root_page(args.memory_root, page_id)
    return payload


def update_root_page(memory_root: Path, page_id: str) -> None:
    paths = memory_paths(memory_root)
    root = read_json(paths["manifest"], {"version": MEMORY_VERSION, "project": "", "assets": {}, "pages": []})
    root["version"] = MEMORY_VERSION
    pages = root.setdefault("pages", [])
    if page_id not in pages:
        pages.append(page_id)
    root["updated_at"] = now_iso()
    write_json(paths["manifest"], root)


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def add_character_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--name", required=True)
    parser.add_argument("--group", default=DEFAULT_ASSET_GROUP)
    parser.add_argument("--version", default=DEFAULT_CHARACTER_VERSION)
    parser.add_argument("--version-type", choices=VERSION_TYPES, default=None)
    parser.add_argument("--description", default="")
    parser.add_argument("--version-description", default="")
    parser.add_argument("--identity-markers", default="")
    parser.add_argument("--project", default=None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--memory-root", type=Path, default=Path("img-memory"))
    parser.add_argument("--project", default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Create the img-memory folder structure.")
    init.add_argument("--project", default=None)

    ensure = subparsers.add_parser("ensure-character", help="Create or refresh a character version manifest.")
    add_character_args(ensure)

    register = subparsers.add_parser("register-image", help="Copy an image into a character version memory slot.")
    add_character_args(register)
    register.add_argument("--kind", required=True)
    register.add_argument("--image", required=True, type=Path)

    missing = subparsers.add_parser("missing", help="Report missing character version memory images.")
    missing.add_argument("--characters", required=True)
    missing.add_argument("--group", default=DEFAULT_ASSET_GROUP)
    missing.add_argument("--version", default=DEFAULT_CHARACTER_VERSION)

    page = subparsers.add_parser("record-page", help="Record page continuity metadata.")
    page.add_argument("--page-id", required=True)
    page.add_argument("--characters", required=True)
    page.add_argument("--group", default=DEFAULT_ASSET_GROUP)
    page.add_argument("--version", default=DEFAULT_CHARACTER_VERSION)
    page.add_argument("--scene-state", default="")
    page.add_argument("--output-image", type=Path)
    page.add_argument("--memory-images-used", default="")
    page.add_argument("--project", default=None)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "init":
        print_json(init_memory(args.memory_root, args.project))
    elif args.command == "ensure-character":
        print_json(ensure_character(args))
    elif args.command == "register-image":
        print_json(register_image(args))
    elif args.command == "missing":
        print_json(missing_report(args.memory_root, split_csv(args.characters), args.group, args.version))
    elif args.command == "record-page":
        print_json(record_page(args))


if __name__ == "__main__":
    main()
