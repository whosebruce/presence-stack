# Obsidian and SMB durable knowledge

Obsidian is the human-readable durable layer. Hermes can read and write Markdown in the same canonical vault when the filesystem is mounted safely.

## Choose one canonical vault

Recommended order:

1. one canonical vault;
2. Obsidian Sync or another conflict-aware sync method for interactive devices;
3. NAS snapshots/backups as protection, not as a second editable truth;
4. Hermes mounts only the dataset/share it needs.

Do not let several machines edit the same SMB-backed vault offline and assume conflict-free merging. Test locking and sync behavior with disposable notes first.

## NAS/share preparation

On the NAS:

- create a dedicated dataset/share for the vault;
- use a dedicated non-admin SMB account;
- grant only required read/write access;
- enable snapshots;
- maintain an independent backup;
- do not expose SMB to the public internet.

Keep the NAS path, username, and password out of Git and chat.

## Linux mount

Install CIFS support using the OS package manager. Create a root-only credentials file locally:

```text
username=<local SMB user>
password=<entered locally>
domain=<optional workgroup/domain>
```

Set mode `0600`. Add an `/etc/fstab` entry locally using your real server/share and UID/GID. A generic pattern is:

```fstab
//server.example/vault  /mnt/obsidian-vault  cifs  credentials=/etc/smb-credentials/obsidian,vers=3.0,uid=1000,gid=1000,file_mode=0660,dir_mode=0770,nofail,x-systemd.automount,_netdev  0  0
```

Do not copy the example literally. Confirm the local user IDs, server name, share, SMB version, and desired permissions first.

Mount and verify:

```bash
findmnt -T /mnt/obsidian-vault
mountpoint -q /mnt/obsidian-vault
python3 - <<'PY'
from pathlib import Path
p=Path('/mnt/obsidian-vault/.presence-stack-write-test')
p.write_text('synthetic test\n')
assert p.read_text() == 'synthetic test\n'
p.unlink()
print('SMB read/write/delete: PASS')
PY
```

Use a disposable filename and verify deletion. Do not run this in an unknown directory without owner approval.

## macOS and Windows

Use the OS SMB client or Obsidian Sync for interactive editing. If the Mac must stay connected across logouts/Fast User Switching, use a carefully reviewed launch service and a dedicated credential store; do not hardcode a password in a public script.

## Point Hermes at the vault

A mounted vault is just a filesystem path. Use:

- a project-specific `AGENTS.md` inside an allowed folder;
- a Hermes profile whose `terminal.cwd` starts in a narrow project folder;
- MCP filesystem access restricted to a specific vault subfolder when appropriate.

Profiles are not sandboxes. If strong isolation is required, use a container/VM and mount only the intended folder.

## Recommended vault structure

```text
Presence/
├── Home.md
├── Profile/
├── Decisions/
├── Projects/
├── Research/
├── Operations/
├── Sources/
└── Logs/
```

Keep raw private archives and large binaries in separate protected storage. Store source links and provenance in notes instead of duplicating everything into prompts.

## Backup acceptance

- snapshot exists;
- independent backup exists;
- one Markdown file was restored to a temporary location and hash/contents verified;
- the agent cannot administer the NAS unless that separate capability is explicitly required;
- no mount credential is tracked by Git.
