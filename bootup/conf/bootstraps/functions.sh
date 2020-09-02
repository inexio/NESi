# Utility functions

# Create a REST API resource, return its ID
function create_resource() {
  req=$1
  endpoint=$2

  id=$(curl -s -d "$req" \
          -H "Content-Type: application/json" \
          -X POST \
          $endpoint | \
       python3 -c "
import sys, json

rsp = {}

try:
    rsp = json.load(sys.stdin)

    sys.stdout.write('%s' % rsp['id'])

except Exception as exc:
    sys.stderr.write('API error #%s (%s)\n' % (rsp.get('status', '?'), rsp.get('message', exc)))
    sys.exit(1)
")

  if [ $? -ne 0 ]; then
      return 1
  fi

  echo $id
}


# Update REST API resource
function update_resource() {
  endpoint=$1

  curl -s -d "{}" \
      -H "Content-Type: application/json" \
      -X PUT \
      $endpoint

  if [ $? -ne 0 ]; then
      return 1
  fi
}

# Upload recording
function upload_recording() {
  endpoint=$1
  filename=$2

  curl -s -d "@$filename" \
      -H "Content-Type: text/plain" \
      -X PUT \
      $endpoint

  if [ $? -ne 0 ]; then
      return 1
  fi
}
