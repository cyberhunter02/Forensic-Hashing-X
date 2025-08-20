<h1 align="center">🕵️‍♂️ Forensic Hashing-X 🔥</h1>

<p align="center">
  <strong>A powerful digital forensics tool for generating and verifying hashes of Text, Files, and Directories with forensic report generation</strong><br>
  <sub>Made with ❤ by <b>Cyber Hunter Warrior</b></sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
  <img src="https://img.shields.io/badge/Platform-Linux%20|%20Windows%20|%20Termux-orange" />
  <img src="https://img.shields.io/badge/Made%20with-Love-red" />
</p> 

## ⚡ Overview

Forensic Hashing-X is a powerful tool designed for digital investigators, law enforcement, and cybersecurity professionals. Its primary function is to generate and verify cryptographic hashes of various digital evidence, including text, files, and entire directories. The tool's core purpose is to ensure the integrity and authenticity of data throughout a forensic investigation.

---

## ✨ Features

* **Text Hashing**: Generate multiple hash values from custom input text.
* **File Hashing**: Upload or specify a file path to generate hash values.
* **Directory Hashing**: Hash all files inside a **ZIP archive** at once.
* **Multi-Algorithm Support**:
    * MD5
    * SHA1
    * SHA224, SHA256, SHA384, SHA512
    * SHA3 (224, 256, 384, 512)
    * BLAKE2B
* **Forensic Report (PDF) Generation** with:
    * Investigator Name
    * Case ID
    * Case Notes / Description
    * ✅ **Signature section (Investigator & Witness)**

---

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/cyberhunter02/Forensic-Hashing-X.git
    ```
2.  **Navigate to the folder:**
    ```bash
    cd Forensic-Hashing-X
    ```
3.  **Install required dependencies:**
    ```bash
    pip install reportlab Flask Werkzeug termcolor --break-system-packages
    ```

---

## ▶️ Usage

1.  **Run the Flask app:**
    ```bash
    python3 app.py
    ```
2.  **Access in your browser:**
    ```
    http://127.0.0.1:5000
    ```

---

## 📄 Example

### Text Hashing Result
**Input Text:** `Test`

| Algorithm | Hash Value |
|:---|:---|
| BLAKE2B | `3d896914f86ae22c48b06140adb4492fa3f8e2686a83cec0c8b1dcd6903168751370078bbd6bbfe02a6ab1df12a19b5991b58e65e243ec279f6a5770b2dd0e31` |
| MD5 | `0cbc6611f5540bd0809a388dc95a615b` |
| SHA1 | `640ab2bae07bedc4c163f679a746f7ab7fb5d1fa` |
| SHA224 | `3606346815fd4d491a92649905a40da025d8cf15f095136b19f37923` |
| SHA256 | `532eaabd9574880dbf76b9b8cc00832c20a6ec113d682299550d7a6e0f345e25` |
| SHA384 | `7b8f4654076b80eb963911f19cfad1aaf4285ed48e826f6cde1b01a79aa73fadb5446e667fc4f90417782c91270540f3` |
| SHA3_224 | `d40cc4f9630f21eef0b185bdd6a51eab1775c1cd6ae458066ecaf046` |
| SHA3_256 | `c0a5cca43b8aa79eb50e3464bc839dd6fd414fae0ddf928ca23dcebf8a8b8dd0` |
| SHA3_384 | `da73bfcba560692a019f52c37de4d5e3ab49ca39c6a75594e3c39d805388c4de9d0ff3927eb9e197536f5b0b3a515f0a` |
| SHA3_512 | `301bb421c971fbb7ed01dcc3a9976ce53df034022ba982b97d0f27d48c4f03883aabf7c6bc778aa7c383062f6823045a6d41b8a720afbb8a9607690f89fbe1a7` |
| SHA512 | `c6ee9e33cf5c6715a1d148fd73f7318884b41adcb916021e2bc0e800a5c5dd97f5142178f6ae88c8fdd98e1afb0ce4c8d2c54b5f37b30b7da1997bb33b0b8a31` |

---

### Forensic Report (PDF)

The generated report is a PDF file that includes the following sections:

* **Investigator Name**
* **Case ID**
* **Case Notes / Description**
* **Generated Hashes** (Algorithm-wise hash values)
* **Signature Section** (for Investigator & Witness)

**Report Format Example:**

Investigator Name: _________________________

Case ID: _________________________

Case Description / Notes: _________________________

Generated Hashes:
(Algorithm-wise hash values)

✍️ Signatures

Investigator Signature: _________________________

Witness Signature: _________________________

---

## 📜 License

This project is developed and maintained by **Cyber Hunter Warrior**.

**Disclaimer:** For educational and forensic investigation purposes only.

## 👨‍💻 Author & Contact

*🧠 Developed By:* Cyber Hunter Warrior

| Platform     | Link |
|--------------|------|
| 🌐 *Website*    | [cyberhunterwarrior.tech](https://cyberhunterwarrior.tech) |
| 📸 *Instagram*  | [@cyberhunterwarrior](https://instagram.com/cyberhunterwarrior) |
| 💼 *LinkedIn*   | [LinkedIn Profile](https://linkedin.com/in/cyberhunterwarrior) |
| ✉ *Email*      | [help.cyberhunterwarrior@gmail.com](help.cyberhunterwarrior@gmail.com) |

---

## 🤝 Contributions

We welcome PRs and new ideas:

- 💡 Suggest enhancements
- 🛠 Fix bugs and improve Tools
- 🌟 Star the repository to show your support!

> Built with 💀 by *Cyber Hunter Warrior*
