import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal

from constants.account_types import AccountType, BankAccountType, InvestmentAccountType

database = "test.db"


def close_database(dbref):
    dbref.sql_close()


@pytest.fixture
def open_database(tmpdir):
    path = tmpdir.join(database)
    dbref = Dbal()
    dbref.sql_connect(path)
    return dbref


@pytest.fixture
def create_accounts_table(open_database):
    dbref = open_database
    dbref.sql_query("DROP TABLE IF EXISTS 'accounts'")
    create_table = (
        'CREATE TABLE IF NOT EXISTS "accounts" '
        + '("record_id" INTEGER NOT NULL,'
        + '"account_type" INTEGER, '
        + '"account_subtype" INTEGER, '
        + '"name" TEXT NOT NULL, '
        + '"description" TEXT, '
        + '"company" TEXT, '
        + '"account_number" TEXT, '
        + '"account_separate" BOOLEAN, '
        + '"hide_in_transaction_list" BOOLEAN, '
        + '"hide_in_account_lists" BOOLEAN, '
        + '"check_writing_avail" BOOLEAN, '
        + '"tax_deferred" BOOLEAN, '
        + '"remarks" TEXT,'
        + 'PRIMARY KEY("record_id" AUTOINCREMENT)'
        + ")"
    )
    result = dbref.sql_query(create_table)
    return dbref


string_too_long = (
    "ShortTermCapitalGainsShortTermCapitalGains"
    + "ShortTermCapitalGainsShortTermCapitalGains"
    + "ShortTermCapitalGainsShortTermCapitalGains"
    + "ShortTermCapitalGainsShortTermCapitalGains"
)


def load_accounts_table(dbref):
    columns = [
        "record_id",
        "account_type",
        "account_subtype",
        "name",
        "description",
        "company",
        "account_number",
        "account_separate",
        "hide_in_transaction_list",
        "hide_in_account_lists",
        "check_writing_avail",
        "tax_deferred",
        "remarks",
    ]
    value_set = [
        [
            "1",
            AccountType.INVESTMENT,
            InvestmentAccountType.SINGLE_FUND,
            "Fidelity Aggressive Growth",
            "sample fund 1",
            "Fidelity Investments",
            "124356987",
            False,
            False,
            False,
            False,
            False,
            "an investment account",
        ],
        [
            "2",
            AccountType.INVESTMENT,
            InvestmentAccountType.BROKERAGE,
            "MerrillLynch IRA",
            "sample fund 2",
            "Fidelity Investments",
            "ml-23654",
            False,
            False,
            False,
            False,
            True,
            "an IRA account",
        ],
        [
            "3",
            AccountType.BANK,
            BankAccountType.SAVINGS,
            "Chase Savings",
            "sample bank 1",
            "Chase Bank",
            "0987654321",
            False,
            False,
            False,
            True,
            False,
            "an bank account",
        ],
        [
            "4",
            AccountType.INVESTMENT,
            InvestmentAccountType.BROKERAGE,
            "MerrillLynch Geneeral",
            "sample fund 3",
            "Fidelity Investments",
            "qvmenrttd",
            False,
            False,
            False,
            True,
            False,
            "an IRA account",
        ],
        [
            "5",
            AccountType.BANK,
            BankAccountType.CHECKING,
            "BA checking",
            "sample bank 2",
            "Bank of America",
            "qvmenrttd",
            False,
            False,
            False,
            True,
            False,
            "a Checking account",
        ],
        [
            "6",
            AccountType.INVESTMENT,
            InvestmentAccountType.SINGLE_FUND,
            "Fidelity Short Term Bond",
            "sample fund 4",
            "Fidelity Investments",
            "0987654321",
            False,
            False,
            True,
            False,
            False,
            "an investment account",
        ],
        [
            "7",
            AccountType.BANK,
            BankAccountType.CD,
            "CD 1",
            "sample bank 3",
            "NFCU",
            "124356987",
            False,
            False,
            False,
            False,
            False,
            "an investment account",
        ],
        [
            "8",
            AccountType.BANK,
            BankAccountType.CD,
            "CD 2",
            "sample bank 4",
            "NFCU",
            "ml-23654",
            False,
            False,
            False,
            False,
            False,
            "an IRA account",
        ],
    ]
    sql_query = {"type": "INSERT", "table": "accounts"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)
