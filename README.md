# Yocto Project + GitHub Actions CI/CD

## 📌 Step-by-Step Yocto + GitHub Actions Learning Plan (2 Months)
This roadmap will take you from **beginner to advanced** in **Yocto Project**, integrating it with **GitHub Actions & Runners**, while incorporating **cybersecurity best practices**.

---

## **🗓️ Week 1-2: Yocto Project Basics**
### 🎯 **Goals:**
✅ Understand **Yocto Project, Poky, OpenEmbedded, BitBake, and Recipes**.  
✅ Build a minimal embedded Linux system using Yocto.  
✅ Learn cybersecurity best practices when working with embedded Linux.

### **📚 Learning Resources:**
- 🎥 [Embedded Linux with Yocto](https://www.youtube.com/watch?v=9vsu67uMcko&list=PLEBQazB0HUyTpoJoZecRK6PpDG31Y7RPB)
- 🎥 [Yocto Project Introduction] (https://www.youtube.com/watch?v=yuE7my3KOpo)
- 🎥 [Yocto Tutorial](https://www.youtube.com/watch?v=5fj05BWryhM&list=PLwqS94HTEwpQmgL1UsSwNk_2tQdzq3eVJ)
- 📖 [Yocto Project Quick Start Guide](https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html)
- 📖 [Yocto Mega-Manual (Reference)](https://docs.yoctoproject.org/ref-manual/index.html)

### **🛠️ Hands-On Tasks:**
✅ Install dependencies (Ubuntu 22.04 recommended).  
✅ Clone **Poky (kirkstone branch)** and set up the build environment.  
✅ Build `core-image-minimal` for **qemuarm64** and run it in QEMU.  
✅ Modify `local.conf` and create a **basic BitBake recipe**.  
✅ **Cybersecurity**: Enable secure boot settings and harden SSH access.

---

## **🗓️ Week 3: Understanding Yocto Layers, Recipes, and SDK**
### 🎯 **Goals:**
✅ Learn how to create and manage **Yocto layers**.  
✅ Write and extend **recipes** for custom packages.  
✅ Use the **Yocto SDK** for secure application development.

### **📚 Learning Resources:**
- 📖 [Yocto Layer Development Guide](https://docs.yoctoproject.org/dev-manual/layers.html)
- 📖 [Yocto Application Development Guide](https://docs.yoctoproject.org/sdk-manual/index.html)

### **🛠️ Hands-On Tasks:**
✅ Create a custom **meta-layer (`meta-myproject`)**.  
✅ Add a **custom BitBake recipe** to compile a **C application**.  
✅ Build and test using the **Yocto SDK**.  
✅ **Cybersecurity**: Apply **compiler hardening flags** and enable **address space layout randomization (ASLR)**.

---

## **🗓️ Week 4: Introduction to GitHub Actions CI/CD**
### 🎯 **Goals:**
✅ Understand **GitHub Actions workflows**.  
✅ Set up a **self-hosted GitHub Runner**.  
✅ Write a basic `.github/workflows/ci.yml` pipeline.

### **📚 Learning Resources:**
- 📖 [GitHub Actions Documentation](https://docs.github.com/en/actions)
- 🎥 [GitHub Actions Crash Course](https://www.youtube.com/watch?v=R8_veQiYBjI)

### **🛠️ Hands-On Tasks:**
✅ Set up a **self-hosted GitHub Runner** securely.  
✅ Write a **CI/CD pipeline** for a simple **Yocto build**.  
✅ **Cybersecurity**: Implement **RBAC (Role-Based Access Control)** for runners.

---

## **🗓️ Week 5: Automating Yocto Builds in GitHub Actions**
### 🎯 **Goals:**
✅ Create a **GitHub Actions CI/CD pipeline** for **Yocto builds**.  
✅ Implement **caching (SSTATE_DIR, DL_DIR)**.  
✅ Generate and store **artifacts (built images)** securely.

### **📚 Learning Resources:**
- 📖 [Optimizing Yocto Builds (Caching & Performance)](https://wiki.yoctoproject.org/wiki/TipsAndTricks/Improving_Performance)

### **🛠️ Hands-On Tasks:**
✅ Modify `.github/workflows/yocto-build.yml` to **automate Yocto builds**.  
✅ Add **caching** for faster builds.  
✅ **Cybersecurity**: Use **code signing** for built images before deployment.

---

## **🗓️ Week 6: Advanced Topics – BSP, Testing, and Deployment**
### 🎯 **Goals:**
✅ Integrate **Board Support Package (BSP) layers**.  
✅ Implement **automated testing**.  
✅ Deploy images to an **embedded device**.

### **📚 Learning Resources:**
- 📖 [Yocto BSP Development Guide](https://docs.yoctoproject.org/bsp-guide/index.html)
- 📖 [Automated Testing in Yocto (pTest)](https://docs.yoctoproject.org/test-manual/index.html)
- 📖 [Deploying Embedded Linux Images](https://elinux.org/Yocto_Install_Image_to_Target)

### **🛠️ Hands-On Tasks:**
✅ Add a **BSP layer** (e.g., **Raspberry Pi** or custom hardware).  
✅ Automate **image deployment** via **TFTP/NFS**.  
✅ Run **automated tests** on built images.  
✅ **Cybersecurity**: Enable **TPM (Trusted Platform Module)** for secure boot.

---

## **🔐 Cybersecurity Best Practices for Yocto & GitHub Actions**

| 🔒 Security Practice         | 🛠️ Implementation |
|------------------------------|------------------|
| 🔑 **Secure SSH Access** | Disable root login and use SSH keys only |
| 🔍 **Static Code Analysis** | Enable **Clang Static Analyzer** for security |
| 📦 **Code Signing** | Sign all built artifacts before deployment |
| 📜 **Immutable File System** | Configure read-only root filesystem |
| 🛡 **RBAC for GitHub Runners** | Restrict runner access to trusted users |
| 🚀 **Security Hardening Flags** | Use `-fstack-protector-strong` and `-D_FORTIFY_SOURCE=2` |

---

## **🚀 Final Outcome**
✔️ **Mastered Yocto + GitHub Actions** for CI/CD.  
✔️ **Automated Yocto builds & deployments** with caching.  
✔️ **Enhanced security** with **secure boot, code signing, and RBAC**.  
