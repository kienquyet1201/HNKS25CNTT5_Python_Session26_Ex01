from abc import ABC, abstractmethod


class BaseAccount(ABC):
    bank_name = "Vietcombank"

    def __init__(self, account_number, owner_name, balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def _set_balance(self, amount):
        self.__balance = amount

    @property
    def owner_name(self):
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, value):
        self.__owner_name = " ".join(value.strip().upper().split())

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented
        return self.balance + other.balance

    def __lt__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented
        return self.balance < other.balance

    @staticmethod
    def validate_account_number(account_number):
        return account_number.isdigit() and len(account_number) == 10

    @classmethod
    def update_bank_name(cls, new_name):
        cls.bank_name = new_name


class SavingsAccount(BaseAccount):
    def __init__(self, account_number, owner_name, interest_rate, balance=0):
        super().__init__(account_number, owner_name, balance)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
        self._set_balance(self.balance + amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")

        penalty = amount * 0.02
        total = amount + penalty

        if total > self.balance:
            raise ValueError("Không đủ số dư")

        self._set_balance(self.balance - total)
        return penalty

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self._set_balance(self.balance + interest)
        return interest


class CreditAccount(BaseAccount):
    def __init__(self, account_number, owner_name, credit_limit, balance=0):
        super().__init__(account_number, owner_name, balance)
        self.credit_limit = credit_limit

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
        self._set_balance(self.balance + amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")

        new_balance = self.balance - amount

        if new_balance < -self.credit_limit:
            raise ValueError("Vượt quá hạn mức thấu chi cho phép")

        self._set_balance(new_balance)


class DigitalPremiumMixin:
    def cashback_reward(self, amount):
        if amount > 5000000:
            return amount * 0.01
        return 0


class HybridAccount(SavingsAccount, DigitalPremiumMixin):
    pass


class VNPayGateway:
    def execute_pay(self, account, amount):
        account.withdraw(amount)
        print(f"[VNPay] Thanh toán {amount:,.0f} VND thành công")


class ViettelMoneyGateway:
    def execute_pay(self, account, amount):
        account.withdraw(amount)
        print(f"[Viettel Money] Thanh toán {amount:,.0f} VND thành công")


def process_payment(payment_gateway, account, amount):
    try:
        payment_gateway.execute_pay(account, amount)
        print("Xác thực thanh toán bằng Duck Typing thành công")
        print(f"Số dư còn lại: {account.balance:,.0f} VND")
    except AttributeError:
        print("Cổng thanh toán không hợp lệ hoặc chưa được tích hợp")
    except Exception as e:
        print(e)


def choose_account(accounts):
    if len(accounts) < 2:
        return None

    print()
    print("DANH SÁCH TÀI KHOẢN")

    for index, account in enumerate(accounts, start=1):
        print(
            f"{index}. {account.account_number} - "
            f"{account.owner_name} "
            f"({account.balance:,.0f} VND)"
        )

    try:
        choice = int(input("Chọn tài khoản: "))
        if 1 <= choice <= len(accounts):
            return accounts[choice - 1]
    except:
        pass

    return None


accounts = []
current_account = None

while True:
    print()
    print("===== VIETCOMBANK DIGIBANK PRO SIMULATOR =====")
    print("1. Mở tài khoản mới")
    print("2. Xem thông tin & Kiểm tra MRO")
    print("3. Giao dịch Nạp / Rút tiền")
    print("4. Áp dụng lãi suất")
    print("5. Gộp tài khoản & So sánh")
    print("6. Thanh toán hóa đơn")
    print("7. Thoát chương trình")

    choice = input("Chọn chức năng (1-7): ")

    if choice == "1":
        print()
        print("1. Savings Account")
        print("2. Credit Account")
        print("3. Hybrid Account")

        account_type = input("Chọn loại tài khoản (1-3): ")

        account_number = input("Nhập số tài khoản 10 chữ số: ")

        if not BaseAccount.validate_account_number(account_number):
            print("Số tài khoản không hợp lệ! Phải gồm đúng 10 chữ số.")
            continue

        owner_name = input("Nhập tên chủ tài khoản: ")

        try:
            if account_type == "1":
                interest_rate = float(
                    input("Nhập lãi suất năm (vd 0.05): ")
                )

                account = SavingsAccount(
                    account_number,
                    owner_name,
                    interest_rate
                )

                print()
                print("Mở tài khoản Tiết kiệm thành công!")

            elif account_type == "2":
                credit_limit = float(
                    input("Nhập hạn mức tín dụng: ")
                )

                account = CreditAccount(
                    account_number,
                    owner_name,
                    credit_limit
                )

                print()
                print("Mở tài khoản Tín dụng thành công!")

            elif account_type == "3":
                interest_rate = float(
                    input("Nhập lãi suất năm (vd 0.05): ")
                )

                account = HybridAccount(
                    account_number,
                    owner_name,
                    interest_rate
                )

                print()
                print("Mở tài khoản Hybrid thành công!")

            else:
                print("Loại tài khoản không hợp lệ")
                continue

            accounts.append(account)
            current_account = account

            print(f"Chủ tài khoản: {account.owner_name}")

        except Exception as e:
            print(e)

    elif choice == "2":
        if current_account is None:
            print("Hệ thống chưa có thông tin tài khoản.")
            continue

        print()
        print("THÔNG TIN TÀI KHOẢN")

        print(
            f"Loại tài khoản: "
            f"{type(current_account).__name__}"
        )

        print(
            f"Ngân hàng: "
            f"{current_account.bank_name}"
        )

        print(
            f"Số tài khoản: "
            f"{current_account.account_number}"
        )

        print(
            f"Chủ tài khoản: "
            f"{current_account.owner_name}"
        )

        print(
            f"Số dư: "
            f"{current_account.balance:,.0f} VND"
        )
        if isinstance(
            current_account,
            (SavingsAccount, HybridAccount)
        ):
            print(
                f"Lãi suất: "
                f"{current_account.interest_rate * 100:.1f}%"
            )
        if isinstance(current_account, CreditAccount):
            print(
                f"Hạn mức tín dụng: "
                f"{current_account.credit_limit:,.0f} VND"
            )
        print()
        print("MRO")
        for cls in type(current_account).mro():
            print(cls.__name__)
    elif choice == "3":
        if current_account is None:
            print("Chưa có tài khoản.")
            continue

        print()
        print("1. Nạp tiền")
        print("2. Rút tiền")
        action = input("Chọn giao dịch (1-2): ")
        try:
            amount = float(input("Nhập số tiền: "))
            if action == "1":
                current_account.deposit(amount)
                print("Nạp tiền thành công")
                if isinstance(current_account, HybridAccount):
                    cashback = current_account.cashback_reward(amount)
                    if cashback > 0:
                        current_account.deposit(cashback)
                        print(
                            f"Hoàn tiền 1%: "
                            f"{cashback:,.0f} VND"
                        )
                print(
                    f"Số dư mới: "
                    f"{current_account.balance:,.0f} VND"
                )
            elif action == "2":
                if isinstance(current_account, SavingsAccount):
                    penalty = current_account.withdraw(amount)
                    print("Rút tiền thành công")
                    print(
                        f"Phí rút trước hạn: "
                        f"{penalty:,.0f} VND"
                    )
                else:
                    current_account.withdraw(amount)
                    print("Rút tiền thành công")

                print(
                    f"Số dư còn lại: "
                    f"{current_account.balance:,.0f} VND"
                )
            else:
                print("Lựa chọn không hợp lệ")
        except Exception as e:
            print(e)
    elif choice == "4":
        if current_account is None:
            print("Chưa có tài khoản.")
            continue
        if isinstance(
            current_account,
            (SavingsAccount, HybridAccount)
        ):
            before = current_account.balance
            interest = current_account.apply_interest()
            print()
            print("Áp dụng lãi suất thành công")
            print(
                f"Số dư trước: "
                f"{before:,.0f} VND"
            )
            print(
                f"Tiền lãi: "
                f"{interest:,.0f} VND"
            )
            print(
                f"Số dư mới: "
                f"{current_account.balance:,.0f} VND"
            )
        else:
            print(
                "Tài khoản tín dụng không hỗ trợ tính lãi"
            )
    elif choice == "5":
        if len(accounts) < 2:
            print("Cần ít nhất 2 tài khoản.")
            continue
        if current_account is None:
            print("Chưa có tài khoản.")
            continue
        print()
        print("SO SÁNH VÀ GỘP TÀI KHOẢN")
        other_account = choose_account(accounts)
        if other_account is None:
            print("Tài khoản không hợp lệ")
            continue
        if other_account == current_account:
            print("Vui lòng chọn tài khoản khác")
            continue
        try:
            if current_account < other_account:
                print(
                    "Tài khoản hiện tại có số dư NHỎ HƠN"
                )
            else:
                print(
                    "Tài khoản hiện tại KHÔNG NHỎ HƠN"
                )
            total = current_account + other_account
            print(
                f"Tổng số dư hai tài khoản: "
                f"{total:,.0f} VND"
            )
        except TypeError:
            print("Không thể thực hiện phép toán")
    elif choice == "6":
        if current_account is None:
            print("Chưa có tài khoản.")
            continue
        print()
        print("1. VNPay")
        print("2. Viettel Money")
        gateway_choice = input(
            "Chọn cổng thanh toán (1-2): "
        )
        try:
            amount = float(
                input("Nhập số tiền hóa đơn: ")
            )
            if gateway_choice == "1":
                gateway = VNPayGateway()
            elif gateway_choice == "2":
                gateway = ViettelMoneyGateway()
            else:
                gateway = object()
            process_payment(
                gateway,
                current_account,
                amount
            )
        except Exception as e:
            print(e)
    elif choice == "7":
        print("Cảm ơn đã sử dụng hệ thống!")
        break
    else:
        print("Lựa chọn không hợp lệ")