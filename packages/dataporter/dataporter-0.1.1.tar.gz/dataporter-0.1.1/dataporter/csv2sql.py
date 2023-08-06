from typing import List, Literal, Optional, Any
from loguru import logger
from fire import Fire
import pandas as pd
from sqlalchemy import create_engine


def _exec_multi_expr(df: pd.DataFrame, exprs: List[str], debug: bool = False) -> pd.DataFrame:
    for expr in exprs:
        if debug:
            logger.info("exec expr: {}", expr)
        df = pd.eval(expr=expr, target=df)

        if debug:
            logger.info("result: {}", df)

    return df


def csv2sql(
    sql_uri: str,
    table_name: str,
    filename: str,
    header: List[int] | Literal["infer"] | None = "infer",
    names: Optional[List[str]] = None,
    sep: str = ",",
    quotechar: str = '"',
    escapechar: Optional[str] = None,
    lineterminator: Optional[str] = None,
    sql_schema: str | None = None,
    sql_data_exists: Literal["fail", "replace", "append"] = "fail",
    read_chunk_size: Optional[int] = None,
    pandas_exprs: List[str] | None = None,
    debug: bool = False,
    ignore_error: bool = False,
    **sql_kwargs: Any
):
    """
    convert csv to sql table.
    :param sql_uri: database uri, according to sqlalchemy uri.
    :param table_name: csv data insert table name.
    :param filename: source csv filename.
    :param header: default first line, also can provide by 'xxx,yyy,bbb' format.
    :param names: specify the headers of csv file, e.g. 'a,b,c,d'.
    :param sep: sep symbol, ',' default.
    :param quotechar: quote char, '"' default.
    :param escapechar: escape char, None default.
    :param lineterminator: line terminator, related to system ('\\n' for linux, '\\r\\n' for Windows, i.e.).
    :param sql_kwargs: other kwargs for sql, it will be pass to sqlalchemy 'create_engine' function.
    :param sql_data_exists: action on data exist in sql db, can be 'fail' or 'replace' or 'append', default 'fail'.
    :param sql_schema: schema on create table, default None (auto generate with no index).
    :param read_chunk_line: if csv file is large, to reduce the memory usage, read csv to memory by trunk of lines.
    :param pandas_exprs: exec multiple pandas expr in order.
    :param debug: if debug mod on, will print every result after exec pandas exprs.
    :param ignore_error: if ignore sql insert error, it may cause loss chunks of data.
    """
    engine = create_engine(url=sql_uri, **sql_kwargs)

    if read_chunk_size is None:
        df = pd.read_csv(
            filename,
            sep=sep,
            names=names,
            header=header,
            quotechar=quotechar,
            escapechar=escapechar,
            lineterminator=lineterminator,
        )
        if pandas_exprs:
            df = _exec_multi_expr(df, exprs=pandas_exprs, debug=debug)
        with engine.begin() as conn:
            df.to_sql(
                name=table_name, con=conn, schema=sql_schema, if_exists=sql_data_exists
            )
    else:
        logger.info("converting csv to sql...")
        trunk_df = pd.read_csv(
            filename,
            sep=sep,
            chunksize=read_chunk_size,
            iterator=True,
            names=names,
            header=header,
            quotechar=quotechar,
            escapechar=escapechar,
            lineterminator=lineterminator,
        )
        with engine.begin() as conn:
            for i, df in enumerate(trunk_df):
                if pandas_exprs:
                    df = _exec_multi_expr(df, exprs=pandas_exprs, debug=debug)
                df: pd.DataFrame
                logger.info(f"writing trunk {len(df)} line...")

                if sql_data_exists == 'append':
                    # if exist strategy is append, all trunk always append
                    current_data_exist = 'append'
                elif sql_data_exists == 'fail':
                    # if exist strategy is fail, it should failed in first trunk
                    # in later trunk, it should be append
                    if i == 0:
                        current_data_exist = 'fail'
                    else:
                        current_data_exist = 'append'
                elif sql_data_exists == 'replace':
                    if i == 0:
                        current_data_exist = 'replace'
                    else:
                        current_data_exist = 'append'
                else:
                    raise ValueError(f"cannot parse current_data_exist value:{sql_data_exists}")

                with logger.catch(message="write to db error, loss chunk.", reraise=not ignore_error):
                    df.to_sql(
                        name=table_name,
                        con=conn,
                        schema=sql_schema,
                        if_exists=current_data_exist,
                    )

        logger.info("done.")


def main():
    Fire(csv2sql)


if __name__ == "__main__":
    main()
