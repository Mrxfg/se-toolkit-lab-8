import json
import os

CONFIG_PATH = "/app/nanobot/config.json"
WORKSPACE_PATH = "/app/nanobot/workspace"

def main():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    config["providers"]["custom"]["apiKey"] = os.environ.get("LLM_API_KEY", "")
    config["providers"]["custom"]["apiBase"] = os.environ.get("LLM_API_BASE_URL", "")
    config["agents"]["defaults"]["model"] = os.environ.get("LLM_API_MODEL", "coder-model")
    config["agents"]["defaults"]["provider"] = "custom"
    config["agents"]["defaults"]["workspace"] = WORKSPACE_PATH

    config["gateway"]["host"] = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    config["gateway"]["port"] = int(os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790"))

    config["channels"]["webchat"] = {
        "enabled": True,
        "host": os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0"),
        "port": int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")),
        "access_key": os.environ.get("NANOBOT_ACCESS_KEY", ""),
        "allow_from": ["*"],
    }

    config["tools"]["mcpServers"] = {
        "lms": {
            "command": "python",
            "args": ["-m", "mcp_lms"],
            "env": {
                "NANOBOT_LMS_BACKEND_URL": os.environ.get("NANOBOT_LMS_BACKEND_URL", ""),
                "NANOBOT_LMS_API_KEY": os.environ.get("NANOBOT_LMS_API_KEY", ""),
            },
        }
    }

    resolved_path = "/app/nanobot/config.resolved.json"
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Resolved config written to {resolved_path}")
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_path, "--workspace", WORKSPACE_PATH])

if __name__ == "__main__":
    main()
