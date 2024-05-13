import configuration as cf
from web3 import Web3
from web3.middleware import geth_poa_middleware 
# импортим всякое
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) 
# наш блокчейн
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# хз че это
contract = w3.eth.contract(address=cf.CONTRACT_ADDRESS, abi=cf.ABI)
# экземпляр контракта

accounts = w3.eth.accounts

def register():
    password = input("Введите пароль: ")
    if len(password) >= 8 and not password.__contains__("123") and not password.__contains__("qwerty") and not password.isalpha() and not password.isdigit():
        account = w3.geth.personal.new_account(password)
        print(f"Ваш публичный ключ: {account}")
        login()
    else:
        print("Пароль слишком лёгкий")

def login():
    public_key = input("Введите ваш публичный ключ: ")
    password = input("Введите пароль: ")
    try:
        w3.geth.personal.unlock_account(public_key, password)
        print("Авторизация прошла успешно!")
        return public_key
    except Exception as e:
        print("Ошибка авторизации: {e}")
        return None

def get_balance(account):
    try:
        balance = contract.functions.getBalance().call({
            'from': account
        })
        print(f"Ваш баланс на смарт-контракте: {balance}")
    except Exception as e:
        print("Ошибка получения баланса: {e}")

def withdraw(account):
    try:
        value = int(input("Введите кол-во WEI для отправки: "))
        tx_hash = contract.functions.withdrawall().transact({ 
            'from' : account,
            'value': value
        })
        print(f"ваша транзакция успешно отправлена. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка отправки WEI: {e}")

def replenishment(account):
    try:
        value = int(input("Введите кол-во WEI для пополнения: "))
        tx_hash = contract.functions.replenishment().transact({ 
            'from' : account,
            'value': value
        })
        print(f"ваша транзакция успешно отправлена. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка отправки WEI: {e}")

def createEstate(account):
    try:
        address = input("Введите адрес: ")
        area = int(input("Введите площадь: "))
        type = int(input("Введите номер типа: "))
        status = bool(input("Введите статус: "))
        id = int(input("Введите id: "))

        tx_hash = contract.functions.addEstate(area, address, type, status, id).transact({ 
            'from' : account,
        })
        print(f"Вы создали недвижимость. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка создания недвижимости: {e}")

def statusEstate(account):
    try:
        id = int(input("Введите id недвижимости: "))

        tx_hash = contract.functions.eastateStatus(id).transact({ 
            'from' : account,
        })
        print(f"Вы изменили статус недвижимости. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка изменения статуса недвижимости: {e}")

def sellEstate(account):
    try:
        id = int(input("Введите id недвижимости: "))
        if str(contract.functions.getEstate().call({'from': account})[id]).__contains__(account):
            print("Вы владелец, нельзя купить")
        else:
            tx_hash = contract.functions.SellEstate(id).transact({ 
                'from' : account,
            })
            print(f"Вы купили недвижимость. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка покупки недвижимости: {e}")

def createAd(account):
    try:
        estateId = int(input("Введите id недвижимости: "))
        cost = int(input("Введите цену: "))
        buyer = input("Введите адрес покупателя: ")
        date = input("Введите дату: ")
        open = bool(input("Введите статус: "))
        adId = int(input("Введите id: "))

        tx_hash = contract.functions.addAD(buyer, cost, estateId, date, open, adId).transact({ 
            'from' : account,
        })
        print(f"Вы создали объявление. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка создания объявления: {e}")

def statusAD(account):
    try:
        id = int(input("Введите id объявления: "))

        tx_hash = contract.functions.adStatus(id).transact({ 
            'from' : account,
        })
        print(f"Вы изменили статус объявления. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка изменения статуса объявления: {e}")

def main():
    account = ""
    while True:
        if account =="" or account == None:
            choice = input("Добро пожаловать в систему! \nЧтобы начать работу войдите или зарегестрруйтесь\n1. Регистрация\n2. Авторизация\n3. Выйти\n")
            match choice:
                case "1":
                    register()
                case "2":
                    account = login()
                case "3":
                    account = ""
                case _:
                    print("Некорректный ввод")
        else:
            choice = input("Выберите: \n1. Просмотр информации\n2. Недвижимость\n3. Объявления\n4. Работа с балансом\n5. Выйти\n")
            match choice:
                case "1":
                    choice = input("Выберите: \n1. Доступная недвижимость\n2. Открытые объявления\n3. Баланс аккаунта\n4. Баланс смарт-контракта\n5. Выйти\n")
                    match choice:
                        case "1":
                            estates = contract.functions.getEstate().call({'from':account})
                            for i in range (len(estates)):
                                print(estates[i])
                                #thisEstate = estates[i]
                                #if thisEstate.active:
                                #    print(f"{i}: Адрес: {thisEstate.estateadress}\nПлощадь: {thisEstate.area}\nТип: {thisEstate.estateType}\nВладелец: {thisEstate.owner}\n\n")
                        case "2":
                            ads = contract.functions.getAd().call({'from':account})
                            for i in range (len(ads)):
                                print(ads[i])
                        case "3":
                            print(f"Баланс аккаунта: {w3.eth.get_balance(account)}")
                        case "4":
                            get_balance(account)
                        case "5":
                            continue
                        case _:
                            print("Выберите от 1 до 5")
                case "2":
                    choice = input("Выберите: \n1. Создать недвижимость\n2. Изменить статус недвижимости\n3. Купить недвижимость\n4. Выйти\n")
                    match choice:
                        case "1":
                            createEstate(account)
                        case "2":
                            statusEstate(account)
                        case "3":
                            sellEstate(account)
                        case "4":
                            continue
                        case _:
                            print("Выберите от 1 до 5")                
                case "3":
                    choice = input("Выберите: \n1. Создать объявление\n2. Изменить статус объявления\n3. Выйти\n")
                    match choice:
                        case "1":
                            createAd(account)
                        case "2":
                            statusAD(account)
                        case "3":
                            continue
                        case _:
                            print("Выберите от 1 до 5") 
                case "4":
                    choice = input("Выберите: \n1. Вывести средства с контракта на счёт\n2. Пополнить баланс с воздуха\n3. Выйти\n")
                    match choice:
                        case "1":
                            withdraw(account)
                        case "2":
                            replenishment(account)
                        case "3":
                            continue
                        case _:
                            print("Выберите от 1 до 5")
                case "5":
                    account = ""
                case _:
                    print("Выберите от 1 до 5")

if __name__ == "__main__":
    main()