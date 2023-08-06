from typer import Typer, run

app = Typer()

def main(name: str, lastname: str = "", formal: bool = False):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        print(f"Good day Ms. {name} {lastname}.")
    else:
        print(f"Hello {name} {lastname}")
        print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")

        

@app.command()
def hello():
    print("Hello.")

@app.command()
def bye(name: str):
    print(f"Bye {name}")
    
if __name__ == "__main__":
    run(main)