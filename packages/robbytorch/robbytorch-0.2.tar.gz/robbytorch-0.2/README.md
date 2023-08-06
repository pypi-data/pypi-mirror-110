# Uwaga!!!

Przed upublicznieniem tego repo trzeba się upewnić, że nie zawiera wrażliwych danych. W szczególności warto przejrzeć notatniki w katalogu `ipython`.

Sama paczka, która jest publicznie dostępna przez `pip`, zawiera wyłącznie pliki z katalogu `src` oraz pliki konfiguracyjne.

Docelowe README dla paczki (które m.in. wyświetla się na https://pypi.org/project/robbytorch/) jest tutaj: [README_pkg.md](README_pkg.md)

# SZKLANKA

W Tej chwili można korzystać z kernela videoresearch albo video - na szklance. Na porcie 5001 jest też postawione MLFlow

## Dodanie env jako kernela na szklance

Trzeba odpalić z poziomu usera `portal`, można to zrobić przez `!` w komórce notatnika:
```
<rezultat odpalenia 'which python' z wnętrza środowiska> -m ipykernel install --prefix=/home/portal/.local --name "<Nazwa kernela, jaka ma być widoczna z poziomu notebooka>"
```

## Inne

- [Package README](README_pkg.md)
- [MLFlow](docs/mlflow.md)
- [git hooks](docs/git_hooks.md)
- [packaging info - jak rozwijać tę paczkę](docs/packaging.md)