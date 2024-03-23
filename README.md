# CypherPass - CS50 Python
#### Video Demo: https://www.youtube.com/watch?v=j1jS4tmkaq0
#### Description:
CipherPass: Secure Password Management at Your command line
This is my project for CS50 Python course. CipherPass is a standalone application designed to empower everyone with secure and effortless password management. Forget juggling complex passwords or relying on insecure online services. CipherPass gives you complete control over your sensitive information, all local-stored in a user-friendly and offline experience.

##### Unparalleled Security:
- Military-Grade Encryption: Your passwords are shielded with robust encryption algorithms, combined with random salts for impenetrable protection. Even if your device falls into the wrong hands, your data remains secure.
- Zero-Knowledge Architecture: CipherPass never stores your master password or any decrypted information on its servers. Everything stays locally encrypted on your device, ensuring complete privacy and control.
- Master Password Protection: Access to your password vault is secured by a powerful master password that only you know. Choose a complex and unique password to safeguard your valuable data.

##### Effortless Management:
- Intuitive Interface: Forget deciphering cryptic commands. CipherPass boasts a user-friendly interface that makes password management simple and intuitive. Add, edit, or remove entries with just a few clicks.
- Powerful Search: Quickly find specific passwords amidst your growing collection with the built-in search functionality. Simply enter a keyword or filter by categories for instant results.

##### Enhanced Features:
- Portable and Secure: Take your password vault wherever you go. CypherPass is a portable application that keeps your data secure, even when you're on the move.
- Random Password Generator: Don't waste time creating strong passwords. CypherPass generates secure and unique combinations that meet the highest security standards.

##### Getting Started:
Download: Visit the official repository to download CypherPass for your operating system.
Launch the Application: run CipherPass.
Create a Master Password: Choose a strong and unique master password and confirm it for access protection.
Start Managing: Begin adding, editing, or removing your password entries. Explore the intuitive interface and discover the features that suit your needs.

CipherPass is a standalone application for secure password management.

#### Usage
        python cypherpass.py
            it will open an interactive menu to manage the passwords

        python cypherpass.py [Options]
            it will run the options to manage the passwords quicker

    Options:
     -h                  : List the usage option.
     -n                  : Create a new database defined on -db:filename. If not included, filename will be assumed as existent.
     -R                  : It will replace an existent file when creating a new database without confirmation.
     -db:filename.pkl    : Define the filename to be used.
     -l                  : List all password tags.
     -k:key              : add the "key" to decode the passwords.
     -t:tag              : select a specific tag.
     -v                  : view the password of a specific tag.
     -a                  : add a new password with a defined tag.
     -rm                 : remove the defined tag.
     -u                  : update the defined tag. It needs -p:password.
     -p:password         : password definition for add/update.
     -pr                 : use a random password

##### Example:
          python cypherpass.py -h
          python cypherpass.py -n -R -db:mypassword.pkl
          python cypherpass.py -db:mypassword.pkl -l
          python cypherpass.py -db:mypassword.pkl -a -r:Gmail -p:mypassword


##### Security Best Practices:
- Choose a Strong Master Password: This is your first line of defense. Make it long, complex, and unique to your password vault.
- Enable Automatic Backups: Regularly backing up your database ensures you can recover your data in case of unexpected events.

Be Cautious with Sharing: Never share your master password or application with anyone.

- More Information:
Visit the GitHub repository for detailed documentation, FAQs, and community support.

##### Future fictures:
- Addition of a Graphic Interface
- Addition of Copy/Paste option
