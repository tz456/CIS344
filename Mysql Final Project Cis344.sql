
-- drop database banks_portal;
create database if not exists banks_portal;

use banks_portal;

create table if not exists accounts(
accountId int primary key not null unique auto_increment,
ownerName varchar(45) not null,
owner_ssn int not null,
balance decimal(10,2) default 0.00,
account_status varchar(45));

create table if not exists Transactions(
transactionId int not null unique auto_increment primary key,
accountID int not null,
foreign key (accountID) references accounts(accountId),
transactionType varchar(45) not null,
transactionAmount decimal(10,2) not null);

insert into accounts (ownerName,owner_ssn,balance,account_status)
values("Maria Jozef", 123456789, 10000.00, "active"), 
("Linda Jones", 987654321, 2600.00, "inactive"), 
("John McGrail", 222222222, 100.50, "active"),
("Patty Luna", 111111111, 509.75, "inactive");

insert into Transactions (accountID,transactionType,transactionAmount)
values(1, "deposit", 650.98), 
(3, "withdraw", 899.87),
(3, "deposit", 350.00);

delimiter #
create procedure accountTransactions(in accountIDD int, out success boolean)
begin
	declare exit handler for sqlexception 
		begin
			set success = false;
			rollback;
		end;
	
    start transaction;
    
	select * from Transactions
    where accountIDD = accountID;
    
    set success = true;
    commit;
end #
delimiter ;

delimiter #
create procedure deposit(in accountIDD int, in amount int, out success boolean)
begin
	declare exit handler for sqlexception 
		begin
			set success = false;
			rollback;
		end;
	
    start transaction;
    
    if exists (select * from accounts where accountId = accountIDD and account_status like "active") then insert into Transactions (accountID,transactionType,transactionAmount)
    values(accountIDD,"deposit",amount);
    
    update accounts
    set balance = balance + amount where accountId = accountIDD and account_status like "active";
    
    set success = true;
    end if;
    commit;
end #
delimiter ;

delimiter #
create procedure withdraw(in accountIDD int, in amount int, out success boolean)
begin
	declare exit handler for sqlexception 
		begin
			set success = false;
			rollback;
		end;
	
    start transaction;
    
    if exists (select * from accounts where accountId = accountIDD and account_status like "active") then insert into Transactions (accountID,transactionType,transactionAmount)
    values(accountIDD,"withdraw",amount);
    
    update accounts
    set balance = balance - amount where accountId = accountIDD and account_status like "active";
    
    set success = true;
    end if;
    commit;
end #
delimiter ;

delimiter #
create procedure deleteAccount(in accountIDD int, out success boolean)
begin
	declare exit handler for sqlexception 
		begin 
			set success = false;
            rollback;
		end;
	
    start transaction;
    
    update accounts
    set account_status = "inactive" where accountId = accountIDD;
    
    set success = true;
    commit;
end #
delimiter ;
