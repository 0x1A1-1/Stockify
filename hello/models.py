from django.db import models
from iexfinance import Stock as IEXStock

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Stock(models.Model):
    name = models.TextField('name')
    code = models.TextField('code')
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)

    # return true if stock object exists or is added, false otherwise
    def add_stock(self, stock_code):

        # check if record already exist
        try:
            Stock.objects.get(code=stock_code)
        except Stock.DoesNotExist:

            # check if insertion is valid
            try:
                user_stock = IEXStock(stock_code)
                new_stock = Stock()
                new_stock.name = user_stock.get_company_name()
                new_stock.code = stock_code
                new_stock.save()
            except:
                return False

        return True

    # return stock object if exist
    def get_stock(self, stock_code):
        try:
            return Stock.objects.get(code=stock_code)
        except:
            return None

    # return true if stock object is deleted, false otherwise
    def remove_stock(self, stock_code):
        try:
            Stock.objects.get(code=stock_code).delete()
            return True
        except:
            return False

    # get price of a specific stock, return False if not valid
    def get_price(self, stock_code):
        try:
            user_stock_price = IEXStock(stock_code).get_price()
            return(stock_code.upper()+" price: $"+str(user_stock_price))
        except:
            return False


    # return a list of stock price
    def get_list_price(self, code_list):

        # check if there is only one code in list
        if len(code_list) == 1:
            return self.get_price(code_list[0])

        # use list to directly query
        user_stocks = IEXStock(code_list)

        try:
            return user_stocks.get_price()
        except:
            return ("No saved stock in record")


class User(models.Model):
    phone = models.TextField('phone')
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)

    # return true if user already exists or is added
    def add_user(self, user_phone):

        # check if record already exist
        try:
            User.objects.get(phone=user_phone)
        except:
            new_user = User()
            new_user.phone = user_phone
            new_user.save()
        return True

    # get a user in the database, return none if not exist
    def get_user(self, user_phone):
        try:
            return User.objects.get(phone=user_phone)
        except:
            return None

    # return true if successfully remove a user from db
    def remove_user(self, user_phone):
        try:
            User.objects.get(phone=user_phone).delete()
            return True
        except:
            return False

class UserXStock(models.Model):
    uid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    sid = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)

    # create new linkage between a user and stock
    def link(self, user_phone, stock_code):
        user_table = User()
        stock_table = Stock()
        target_user = User.objects.get(phone=user_phone)
        target_stock = Stock.objects.get(code=stock_code)

        # Verify both user and stock are valid for linking purposes
        if target_user and target_stock:
            try:
                UserXStock.objects.get(uid=target_user.id, sid=target_stock.id)
                return True
            except:
                new_link = UserXStock()
                new_link.uid = target_user
                new_link.sid = target_stock
                new_link.save()
                return True
        else:
            return False

    # Unlink existing user relation
    def unlink(self, user_phone, stock_code):
        target_user = User().get_user(user_phone)
        target_stock = Stock().get_stock(stock_code)

        # Verify both user and stock are valid for unlinking purposes
        if target_user and target_stock:
            try:
                UserXStock.objects.get(uid=target_user.id, sid=target_stock.id).delete()
                return True
            except Exception as e:
                return False
        else:
            return False

    # return the whole list of prices related
