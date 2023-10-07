class Python:
    type = "язык программирования"
    version = ""
    def __init__(self, py_version):
        self.version = py_version
    def launch(self): print(f"Python v {self.version} has been started")

python11 = Python('3.11.2')
python11.launch()

python10 = Python('3.10.3')
python10.launch()
