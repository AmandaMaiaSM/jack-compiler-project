def read_file(file_path):
    texto = ""
    try: 
        with open(file_path, "r", encoding="utf-8") as f:
            texto = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

    return texto
