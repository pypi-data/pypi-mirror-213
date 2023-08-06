import typer
import commands.python
import commands.js
import commands.cpp

app = typer.Typer()
app.add_typer(commands.python.app, name="python")
app.add_typer(commands.js.app, name="js")
app.add_typer(commands.cpp.app, name='cpp')

if __name__  == '__main__':
    app()
