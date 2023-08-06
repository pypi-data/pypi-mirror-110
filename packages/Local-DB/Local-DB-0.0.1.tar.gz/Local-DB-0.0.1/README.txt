A local DB project. Reminds PyMongo but being used locally with json files.

Operators:

find_one = returns a record who match the condition
find_many =  returns all records who match the condition

update_one = updates a record who match the condition
update_many =  updates all records who match the condition

delete_one = deletes a record who match the condition
delete_many =  deletes all records who match the condition


//example of initialization

db = Local_db("PATH TO LOCAL JSON FILE")

//after that you can use all the operators.