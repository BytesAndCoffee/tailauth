import znc
import os
import json
import subprocess
from datetime import datetime

class tailauth(znc.Module):
    module_types = [znc.CModInfo.GlobalModule]
    description = "Auto-authenticate ZNC users from verified Tailnet clients only"

    def OnLoginAttempt(self, auth):
        ip_str = auth.GetRemoteIP()
        user_str = auth.GetUsername()
        self.log(f"[{datetime.now().isoformat()}] Login attempt: user='{user_str}', ip='{ip_str}'")

        hostname = self.get_tailnet_hostname(ip_str)
        if hostname:
            user = znc.CZNC.Get().FindUser(user_str)
            if user:
                self.log(f"[{datetime.now().isoformat()}] ✅ Authenticated Tailnet device '{hostname}' for user '{user.GetUserName()}'")
                auth.AcceptLogin(user)
                return znc.HALT
            else:
                self.log(f"[{datetime.now().isoformat()}] ⚠️ Authenticated device '{hostname}', but user '{user_str}' not found")
        else:
            self.log(f"[{datetime.now().isoformat()}] ❌ IP {ip_str} not found in authenticated Tailnet clients")

        return znc.CONTINUE

    def get_tailnet_hostname(self, ip_str):
        try:
            output = subprocess.check_output(
                ['tailscale', 'status', '--json'],
                stderr=subprocess.DEVNULL,
                timeout=2,
                text=True
            )
            data = json.loads(output)
            for peer in data.get("Peer", {}).values():
                if ip_str in peer.get("TailscaleIPs", []):
                    return peer.get("HostName", "unknown-host")
            # Also check the local device
            for local_ip in data.get("Self", {}).get("TailscaleIPs", []):
                if ip_str == local_ip:
                    return data.get("Self", {}).get("HostName", "local-device")
        except Exception as e:
            self.log(f"[{datetime.now().isoformat()}] ⚠️ Error reading tailscale status: {e}")
        return None

    def log(self, message):
        path = os.path.join(self.GetSavePath(), "tailauth.log")
        try:
            with open(path, "a") as f:
                f.write(message + "\n")
        except Exception as e:
            self.PutModule(f"[tailauth] Logging failed: {e}")
