"""CLI mínimo para operar sobre o CSV local (listar, inserir, atualizar, deletar, exportar)."""
import argparse
import pandas as pd
from storage import load_csv, save_csv
from finance import inserir_transacao, atualizar_transacao, deletar_transacao, atualizar_montantes


DATA_FILE = "data/transacoes_v2.csv"




def cmd_list(args):
    df = load_csv(DATA_FILE)
    if df.empty:
        print("Nenhuma transação encontrada.")
        return
    print(df.sort_values(by="data").to_string(index=False))




def cmd_add(args):
    df = load_csv(DATA_FILE)
    df = inserir_transacao(df, args.data, args.tipo, args.valor, args.juros_dia, args.descricao)
    save_csv(df, DATA_FILE)
    print("Inserido com sucesso")




def cmd_update(args):
    df = load_csv(DATA_FILE)
    df = atualizar_transacao(df, args.id, **{k:v for k,v in vars(args).items() if k in ["data","tipo","valor","juros_dia","descricao"] and v is not None})
    save_csv(df, DATA_FILE)
    print("Atualizado")




def cmd_delete(args):
    df = load_csv(DATA_FILE)
    df = deletar_transacao(df, args.id)
    save_csv(df, DATA_FILE)
    print("Deletado")




def cmd_update_rendimentos(args):
    df = load_csv(DATA_FILE)
    df = atualizar_montantes(df, referencia=None)
    save_csv(df, DATA_FILE)
    print("Montantes atualizados")




parser = argparse.ArgumentParser(prog="tcf-v2")
sub = parser.add_subparsers()


p = sub.add_parser("list")
p.set_defaults(func=cmd_list)


p = sub.add_parser("add")
p.add_argument("data")
p.add_argument("tipo")
p.add_argument("valor", type=float)
p.add_argument("--juros_dia", type=float, default=None)
p.add_argument("--descricao", default=None)
p.set_defaults(func=cmd_add)


p = sub.add_parser("update")
p.add_argument("id", type=int)
p.add_argument("--data")
p.add_argument("--tipo")
p.add_argument("--valor", type=float)
p.add_argument("--juros_dia", type=float)
p.add_argument("--descricao")
p.set_defaults(func=cmd_update)


p = sub.add_parser("delete")
p.add_argument("id", type=int)
p.set_defaults(func=cmd_delete)


p = sub.add_parser("update_rendimentos")
p.set_defaults(func=cmd_update_rendimentos)


if __name__ == "__main__":
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()