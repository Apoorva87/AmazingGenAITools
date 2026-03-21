#!/bin/bash

SRC="obsidian-vault/"
DEST="/Users/akarnik/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyLife/AI_Learn/"

read -p "Mode? (new/update): " MODE

ARGS=""
if [[ "$MODE" == "new" ]]; then
  ARGS="-avh --ignore-existing"
elif [[ "$MODE" == "update" ]]; then
  ARGS="-avh --update"
else
  echo "Usage: choose 'new' or 'update'"
  exit 1
fi

echo "🔍 Dry run preview..."
rsync $ARGS \
  --exclude='.git' \
  --exclude='.obsidian/workspace*' \
  --exclude='.DS_Store' \
  --dry-run \
  "$SRC" "$DEST"

echo ""
echo "🧠 Showing diffs for changed files (if any)..."

# Get list of files that would change
CHANGED_FILES=$(rsync -rcn $ARGS \
  --exclude='.git' \
  --exclude='.obsidian/workspace*' \
  --exclude='.DS_Store' \
  "$SRC" "$DEST" | awk '{print $2}')

for FILE in $CHANGED_FILES; do
  SRC_FILE="$SRC/$FILE"
  DEST_FILE="$DEST/$FILE"

  if [[ -f "$SRC_FILE" && -f "$DEST_FILE" ]]; then
    echo "=============================="
    echo "Diff: $FILE"
    diff -u "$DEST_FILE" "$SRC_FILE" | head -n 200
  fi
done

echo ""
read -p "Proceed with sync? (y/n): " confirm

if [[ "$confirm" == "y" ]]; then
  echo "🚀 Syncing..."
  rsync $ARGS \
    --exclude='.git' \
    --exclude='.obsidian/workspace*' \
    --exclude='.DS_Store' \
    "$SRC" "$DEST"
  echo "✅ Done."
else
  echo "❌ Aborted."
fi

