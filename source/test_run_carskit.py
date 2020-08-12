from ..run_carskit import Runner

def test_run_engine():
    runner = Runner('C:\\Users\\Waguinho\\Documents\\pesquisa\\CARSKit_Interface\\source\\CARSKit')
    OK_CODE = 0
    assert runner.run_engine() == OK_CODE