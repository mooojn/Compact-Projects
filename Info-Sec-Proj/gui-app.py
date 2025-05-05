import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def apply_ssh_security():
    try:
        # Apply SSH security restrictions by modifying the sshd_config file
        with open("/etc/ssh/sshd_config", "a") as ssh_config:
            ssh_config.write("\nMaxAuthTries 1\n")
            ssh_config.write("MaxSessions 2\n")
            ssh_config.write("LoginGraceTime 30\n")
        
        # Restart SSH service to apply changes
        subprocess.run(["systemctl", "restart", "ssh"], check=True)
        messagebox.showinfo("Success", "SSH security settings applied and SSH service restarted.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to apply SSH settings: {e}")

def apply_password_policy():
    try:
        # Install pam_pwquality if not present
        result = subprocess.run(["dpkg", "-s", "libpam-pwquality"], stdout=subprocess.DEVNULL)
        if result.returncode != 0:
            subprocess.run(["apt", "update"], check=True)
            subprocess.run(["apt", "install", "-y", "libpam-pwquality"], check=True)

        pam_path = "/etc/pam.d/common-password"
        updated_lines = []
        found = False

        # Modify pam configuration for password complexity and length
        with open(pam_path, "r") as file:
            for line in file:
                if "pam_pwquality.so" in line:
                    line = "password requisite pam_pwquality.so retry=3 minlen=6 reject_username difok=3 ucredit=-1 lcredit=-1 dcredit=-1 maxrepeat=2 enforce_for_root\n"
                    found = True
                updated_lines.append(line)

        if not found:
            updated_lines.append("password requisite pam_pwquality.so retry=3 minlen=6 reject_username difok=3 ucredit=-1 lcredit=-1 dcredit=-1 maxrepeat=2 enforce_for_root\n")

        with open(pam_path, "w") as file:
            file.writelines(updated_lines)

        messagebox.showinfo("Success", "Password policy applied: Minimum length = 6, enforced complexity rules.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to apply password policy: {e}")

def generate_password():
    import random
    import string
    length = 12
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choices(chars, k=length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
def create_new_user():
    # Get username and password from input fields
    username = username_entry.get()
    password = password_entry.get()

    if len(password) < 6:
        messagebox.showerror("Password Error", "Password must be at least 6 characters long!")
        return
    
    try:
        # Create new user
        subprocess.run(["sudo", "adduser", username, "--gecos", "", "--disabled-password"], check=True)
        
        # Set the password for the new user (using a shell to ensure correct format)
        subprocess.run(f"echo '{username}:{password}' | sudo chpasswd", shell=True, check=True)

        messagebox.showinfo("Success", f"User '{username}' created successfully with a strong password.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to create user: {e}")


# GUI Setup
app = tk.Tk()
app.title("🔐 Linux Security Hardener")
app.geometry("400x400")
tk.Label(app, text="Security Configuration Tool", font=("Helvetica", 16, "bold")).pack(pady=10)

# SSH Security Button
tk.Button(app, text="Apply SSH Login Restrictions", command=apply_ssh_security, bg="lightblue").pack(pady=5)

# Password Policy Button
tk.Button(app, text="Apply Password Policy", command=apply_password_policy, bg="lightgreen").pack(pady=5)

# User Creation Section
tk.Label(app, text="Create New User (Enter Username and Password)").pack(pady=10)
tk.Label(app, text="Username:").pack()
username_entry = tk.Entry(app, width=30, font=("Courier", 12))
username_entry.pack()

tk.Label(app, text="Password:").pack()
password_entry = tk.Entry(app, width=30, font=("Courier", 12))
password_entry.pack()

tk.Button(app, text="Create User", command=create_new_user, bg="lightcoral").pack(pady=10)

# Generate Password Section
tk.Label(app, text="Generate Strong Password:").pack(pady=10)
tk.Button(app, text="Generate Password", command=generate_password, bg="orange").pack(pady=5)

app.mainloop()
