from typing import List, Callable, Union, Dict, Any, Optional
from pydantic import validate_arguments
import pandas as pd
from dukto.cus_types import col_names, proc_function, new_names
from pandera.typing import DataFrame
from dukto.base_processor import BaseProcessor
from dukto.logger import logger


class ColProcessor(BaseProcessor):
    @validate_arguments
    def __init__(
        self,
        name: col_names,
        funcs: proc_function,
        new_name: new_names = None,
        funcs_test: Dict[Any, Any] = {},
        run_test_cases: bool = False,
        suffix: str = "",
        drop: bool = False,
    ):
        self.funcs = [funcs] if not isinstance(name, list) else funcs
        self.name = [name] if isinstance(name, str) else name
        self.new_name = new_name if new_name else name
        self.funcs_test = funcs_test
        self.suffix = suffix
        self.run_test_cases = run_test_cases
        self.drop = drop

    @staticmethod
    def run_functions(data: DataFrame, name: str, functions: List[Callable]):
        temp = data[name].copy()
        for func in functions:
            temp = temp.apply(func)
        return temp

    def types(self):
        # if new_name is not provided  use name(s)
        if self.new_name == self.name:
            self.new_name = {n: n for n in self.name}

        # make sure if name is a list new_name is a dict
        # if isinstance(self.name, List) and isinstance(self.new_name, str):
        #     raise TypeError(
        #         f"""if you're applying the ColProcessor to many columns
        #         new_name should be of type dict not {type(self.new_name)}
        #         Example(new_name={{"name":"new_name"}})"""
        #     )

        if isinstance(self.name, str):  # check if name is string and if so turn it into a list
            self.name = [self.name]

        # check if new name is a string and if so turn into a dict
        if isinstance(self.new_name, str):
            self.new_name = {self.new_name: self.new_name}

        # update new_name and use the name for the missing new_name(s)
        if isinstance(self.new_name, dict):
            not_in = set(self.name) - set(self.new_name.keys())
            self.new_name.update({n: n for n in not_in})

    # @log_step
    def run(self, data: DataFrame) -> DataFrame:
        self.types()

        for n in self.name:
            new_name = self.new_name[n] if isinstance(self.new_name, dict) else self.new_name
            data[new_name + self.suffix] = ColProcessor.run_functions(data, n, self.funcs)

        return data.drop(self.name, axis=1) if self.drop else data

    def test_res_printer(self, res: Optional[int] = None) -> None:
        class_name = self.__class__.__name__
        cols = ColProcessor.name_formatter(self.name)
        if res == None:  # no tests
            print(f"{class_name: <2} {cols: <30} test cases NOT FOUND.")
        elif res == 0:  # failed
            print(f"{class_name: <2} {cols: <30} test cases Failed! 😒")
        elif res == 1:
            print(f"{class_name: <2} {cols: <30} test cases PASSED! 😎")

    def test(self):
        # TODO: {"input": np.nan}  doesn't work
        # TODO: refactor this function
        # TODO: show the failing cases
        # TODO: tests fail if we changed the name of the Column (try to run the test in the pipe after the run mathod)
        data = pd.Series(data=self.funcs_test).to_frame().reset_index()
        data.columns = ["in", "out"]
        out_val = ColProcessor.run_functions(data, "in", self.funcs)
        mismatches = data[data["out"] != out_val]
        if not self.funcs_test:
            self.test_res_printer()
        elif mismatches.empty:  # if empty them all cases matched
            self.test_res_printer(res=1)
        else:
            self.test_res_printer(res=0)
            print("=>", mismatches)

    @staticmethod
    def name_formatter(name):
        return f"({', '.join(name) if isinstance(name, list) else name})"

    def __repr__(self):
        return f"ColProcessor({', '.join(self.name)})"


class MultiColProcessor(BaseProcessor):
    ## TODO: add testing
    @validate_arguments
    def __init__(self, funcs: List, funcs_test: Dict = {}, name: Union[List, str] = ""):
        self.funcs = funcs
        self.funcs_test = funcs_test
        self.name = [name] if isinstance(name, str) else name

    # @log_step
    def run(self, data: DataFrame) -> DataFrame:
        for f in self.funcs:
            data = data.pipe(f)
        return data

    def test(self):
        print("Multi test not implemented yet")

    def __repr__(self):
        return f"MultiColProcessor({', '.join(self.name)})"


class Transformer(BaseProcessor):
    # TODO: add testing
    # TODO: name_from_func use suffix to select columns
    # example: name_from_func=lambda x:[i for i in x if '_new' in i]
    @validate_arguments
    def __init__(
        self,
        transformers: Union[List, Callable],
        name: Union[str, List, None] = None,
        name_from_func: Optional[Callable] = None,
        **kwargs,
        # TODO add parser for kwargs in case there's more than one Transformer
    ):
        self.transformers = [transformers] if isinstance(transformers, Callable) else transformers
        self.name = [name] if isinstance(name, str) else name
        self.name_from_func = name_from_func
        self.kwargs = kwargs

    def run(self, data: DataFrame) -> DataFrame:
        if self.name_from_func:
            self.name = self.name_from_func(data.columns.tolist())
        for t in self.transformers:
            trans = t(variables=self.name, **self.kwargs)
            data = trans.fit_transform(X=data)
        return data

    def test(self):
        print("transformer test not implemented yet")

    def __repr__(self):
        # TODO add more informative repr and __str__ cuz this shit sucks
        return f"Transformer()"
