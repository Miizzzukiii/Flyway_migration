import subprocess
import os

# Путь к директории с миграциями
MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), 'migrations/sql')

# Функция для выполнения команды Flyway
def run_flyway_command(command):
    try:
        result = subprocess.run(
            ['flyway', command, f'-locations=filesystem:{MIGRATIONS_DIR}'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error during '{command}':", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to execute Flyway command: {e}")
        return False

# Функция для выполнения миграций
def migrate():
    print("Running migrations...")
    if run_flyway_command('migrate'):
        print("Migrations completed successfully.")
    else:
        print("Migrations failed.")

# Функция для проверки состояния миграций
def info():
    print("Checking migration status...")
    if run_flyway_command('info'):
        print("Migration status checked successfully.")
    else:
        print("Failed to check migration status.")

# Функция для отката миграций (требуется платная версия Flyway)
def undo():
    print("Undoing last migration...")
    if run_flyway_command('undo'):
        print("Migration undone successfully.")
    else:
        print("Failed to undo migration.")

# Основная функция
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Manage database migrations with Flyway.")
    parser.add_argument('command', choices=['migrate', 'info', 'undo'], help="The Flyway command to execute.")

    args = parser.parse_args()

    if args.command == 'migrate':
        migrate()
    elif args.command == 'info':
        info()
    elif args.command == 'undo':
        undo()

if __name__ == "__main__":
    main()