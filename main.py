import os
import shutil

class XamppMySqlIssueResolver:
    def __init__(self, xampp_path):
        self.xampp_path = xampp_path
        self.mysql_path = os.path.join(xampp_path, 'mysql')

    def resolve_mysql_issue(self):
        print("Resolving MySQL issue...")
        if not os.path.exists(self.mysql_path):
            print("MySQL directory not found. Please check your XAMPP installation path.")
            return
        
        mysql_data_path = os.path.join(self.mysql_path, 'data')
        if not os.path.exists(mysql_data_path):
            print("MySQL data directory not found. Reinstall the Xampp")
            return
        
        mysql_error_log = os.path.join(self.mysql_path, 'data', 'mysql_error.log')
        if os.path.exists(mysql_error_log):
            with open(mysql_error_log, 'r') as log_file:
                errors = log_file.readlines()
                if errors:
                    print("MySQL Error Log:")
                    for error in errors:
                        print(error.strip())
                else:
                    print("No errors found in MySQL error log.")
        else:
            print("MySQL error log not found. Please check your XAMPP installation.")

        # Step 1: Rename mysql/data to mysql/data_old
        data_old_path = os.path.join(self.mysql_path, 'data_old')
        if not os.path.exists(data_old_path):
            os.rename(mysql_data_path, data_old_path)
            print("Renamed 'data' to 'data_old'.")
        else:
            print("'data_old' already exists. Skipping rename.")

        # Step 2: Copy mysql/backup to mysql/data
        backup_path = os.path.join(self.mysql_path, 'backup')
        if not os.path.exists(backup_path):
            print("Backup folder not found. Cannot proceed.")
            return
        shutil.copytree(backup_path, mysql_data_path, dirs_exist_ok=True)
        print("Copied 'backup' to 'data'.")

        # Step 3: Copy user database folders from data_old to data
        exclude_folders = {'mysql', 'performance_schema', 'phpmyadmin'}
        for item in os.listdir(data_old_path):
            src = os.path.join(data_old_path, item)
            dst = os.path.join(mysql_data_path, item)
            if os.path.isdir(src) and item not in exclude_folders:
                shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"Copied database folder '{item}' to new data directory.")

        # Step 4: Copy ibdata1 file
        ibdata1_src = os.path.join(data_old_path, 'ibdata1')
        ibdata1_dst = os.path.join(mysql_data_path, 'ibdata1')
        if os.path.exists(ibdata1_src):
            shutil.copy2(ibdata1_src, ibdata1_dst)
            print("Copied 'ibdata1' file to new data directory.")
        else:
            print("'ibdata1' file not found in data_old.")

        # Step 5: Clear the console screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print("MySql issue resolved successfully.")
        print("Please restart the MySQL service in XAMPP Control Panel.")
        return
    


def main():
    print("XAMPP MySQL Issue Resolver Started ...")
    path = input("Enter the path to your XAMPP installation (default is C:\\xampp): ")
    if not path:
        path = "C:\\xampp"

    resolver = XamppMySqlIssueResolver(path)
    resolver.resolve_mysql_issue()

if __name__ == "__main__":
    main()