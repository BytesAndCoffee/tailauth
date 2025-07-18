import znc
import ipaddress
import os
from datetime import datetime

class tailauth(znc.Module):
    module_types = [znc.CModInfo.GlobalModule]
    description = "Auto-auth users connecting from Tailscale (100.64.0.0/10)"
    wiki_page = "tailauth"

    def OnLoginAttempt(self, auth):
        ip_str = auth.GetRemoteIP()
        user_str = auth.GetUsername()
        self.log(f"Login: user='{user_str}', ip='{ip_str}'")

        try:
            ip = ipaddress.IPv4Address(ip_str)
            if ip in ipaddress.IPv4Network("100.64.0.0/10"):
                user = znc.CZNC.Get().FindUser(user_str)
                if user:
                    self.log(f"Accepted user '{user.GetUserName()}' from {ip_str}")
                    auth.AcceptLogin(user)
                    return znc.HALT
                else:
                    self.log(f"User '{user_str}' not found")
        except Exception as e:
            self.log(f"IP parse error from '{ip_str}': {e}")

        return znc.CONTINUE

    def log(self, message):
        path = os.path.join(self.GetSavePath(), "tailauth.log")
        try:
            with open(path, "a") as f:
                f.write(f"[{datetime.now().isoformat()}] {message}\n")
        except Exception as e:
            self.PutModule(f"[tailauth] Failed to write log: {e}")
