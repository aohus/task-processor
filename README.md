# task-processor

[API 문서](https://www.notion.so/d4505f5fe9554da9832a60ea1483cb6b?pvs=4)

### Run Django dev server

1. clone git repository
   ```bash
   git clone https://github.com/aohus/task-processor.git
   ```
2. make venv && activate

   ```bash
   cd test-processor
   bash conv/make_venv.sh venv
   source venv/bin/activate
   ```

   - python version 3.11 required. If you prefer a different Python version, you can adjust the settings in the [conv/make_venv.sh] file.
   - To install Python 3.11, follow these steps:

   ```bash
   # ubuntu
   sudo apt install python3.11
   sudo apt install python3.11-venv

   # macos
   brew update
   brew install python3.11
   ```

3. go to apps repository && run dev server
   ```bash
   cd apps/
   python3 manage.py runserver
   ```
