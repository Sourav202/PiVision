#!/bin/sh
PATH=$PATH:/usr/bin:/bin:/sbin:/usr/sbin

PC_IP=172.20.10.5
PORT=8000
CMD_URL="http://$PC_IP:$PORT/next_cmd"
UPLOAD_URL="http://$PC_IP:$PORT/upload"

CAM_UNIT=1
OUT_DIR="/data/share/sensor"

LOCK="/tmp/record_agent.lock"

# Prevent running multiple copies
if [ -f "$LOCK" ]; then
  echo "ERROR: record_agent already running (lock exists: $LOCK)"
  echo "If you're sure it's not running: rm -f $LOCK"
  exit 1
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"; exit' INT TERM EXIT

# Ensure recorder exists in PATH
if ! command -v camera_example4_record >/dev/null 2>&1; then
  echo "ERROR: camera_example4_record not found in PATH."
  echo "Try: which camera_example4_record"
  exit 1
fi

newest_mp4() {
  ls -t "$OUT_DIR"/*.mp4 2>/dev/null | head -n 1
}

echo "Polling PC for commands at $CMD_URL"
echo "Recording via: camera_example4_record -u $CAM_UNIT"
echo "Output dir:   $OUT_DIR"
echo "Upload via:   curl -T <file> $UPLOAD_URL"

while true; do
  CMD=$(curl -s "$CMD_URL" | tr -d '\r\n')

  if [ "$CMD" = "" ]; then
    echo "WARN: empty /next_cmd response (network hiccup?)"
    sleep 2
    continue
  fi

  if [ "$CMD" = "NOOP" ]; then
    sleep 1
    continue
  fi

  echo "=============================="
  echo "Got command: $CMD"
  echo "=============================="

  case "$CMD" in
    RECORD*)
      SECS=$(echo "$CMD" | awk '{print $2}')
      if [ "$SECS" = "" ]; then SECS=5; fi

      BEFORE=$(newest_mp4)
      echo "Newest before: $BEFORE"
      echo "Recording for $SECS seconds..."

      # Non-interactive start/stop:
      # keypress to start, sleep, keypress to stop
      ( printf "\n"; sleep "$SECS"; printf "\n" ) | camera_example4_record -u "$CAM_UNIT"
      RC=$?
      echo "Record exit code: $RC"

      AFTER=$(newest_mp4)
      echo "Newest after:  $AFTER"

      if [ "$AFTER" = "" ]; then
        echo "ERROR: no mp4 found in $OUT_DIR"
        continue
      fi
      if [ "$AFTER" = "$BEFORE" ]; then
        echo "ERROR: newest mp4 did not change; record may have failed."
        continue
      fi

      echo "Uploading $AFTER ..."
      RESP=$(curl -s -S -T "$AFTER" "$UPLOAD_URL")
      echo ""
      RC2=$?
      echo "Server response: $RESP"
      echo "Upload exit code: $RC2"
      ;;
    *)
      echo "Unknown command: $CMD"
      ;;
  esac
done
