# Go Examples

High-performance CLI tools for PAN-OS firewall operations built with Go and the `pango` SDK.

## Projects

| Category | Count | Description |
|----------|-------|-------------|
| [PAN-OS Tools](panos.md) | 2 | Commit and session analysis CLI tools |
| [Panorama Tools](panorama.md) | 1 | Mock API server (placeholder) |

## Why Go?

Go produces standalone binaries with no runtime dependencies, making these tools easy to distribute and run on any system. The `pango` SDK provides native Go access to the PAN-OS XML API.

## Common Setup

```bash
# Download dependencies
go mod download

# Run directly
go run main.go

# Or build a binary
go build -o tool-name .
./tool-name
```

!!! tip "`go run` vs `go build`"
    `go run` compiles and runs in one step (good for testing). `go build` creates a standalone binary you can copy anywhere and run without Go installed.
