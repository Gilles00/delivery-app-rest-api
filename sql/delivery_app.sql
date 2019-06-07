-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema delivery_app_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema delivery_app_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `delivery_app_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `delivery_app_db` ;

-- -----------------------------------------------------
-- Table `delivery_app_db`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`user` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`user` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_firstname` VARCHAR(45) NOT NULL,
  `user_lastname` VARCHAR(45) NOT NULL,
  `email` VARCHAR(100) NULL,
  `location` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `user_profilepicture` VARCHAR(100) NOT NULL,
  `user_gender` CHAR NOT NULL,
  `user_dateOfBirth` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `delivery_app_db`.`rider`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`rider` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`rider` (
  `rider_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `rider_firstname` VARCHAR(45) NOT NULL,
  `rider_lastname` VARCHAR(45) NOT NULL,
  `rider_email` VARCHAR(100) NULL,
  `rider_password` VARCHAR(255) NOT NULL,
  `rider_nationality` VARCHAR(45) NOT NULL,
  `rider_dateofbirth` DATE NOT NULL,
  `rider_profilepicture` VARCHAR(100) NOT NULL,
  `rider_gender` CHAR NOT NULL,
  PRIMARY KEY (`rider_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `delivery_app_db`.`rider_Bank _Account`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`rider_Bank _Account` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`rider_Bank _Account` (
  `rider_account_number` VARCHAR(45) NOT NULL,
  `rider_holdername` VARCHAR(45) NOT NULL,
  `rider_id` INT UNSIGNED NOT NULL,
  INDEX `fk_rider_bank_rider_personal_idx` (`rider_id` ASC),
  CONSTRAINT `fk_rider_bank_rider_personal`
    FOREIGN KEY (`rider_id`)
    REFERENCES `delivery_app_db`.`rider` (`rider_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `delivery_app_db`.`vehicle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`vehicle` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`vehicle` (
  `vehicle_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `vehicle_licensenumber` VARCHAR(45) NOT NULL,
  `vehicle_number` VARCHAR(45) NOT NULL,
  `vehicle_model` VARCHAR(45) NOT NULL,
  `rider_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`vehicle_id`),
  INDEX `fk_vehicle_detail_rider_personal1_idx` (`rider_id` ASC),
  CONSTRAINT `fk_vehicle_detail_rider_personal1`
    FOREIGN KEY (`rider_id`)
    REFERENCES `delivery_app_db`.`rider` (`rider_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `delivery_app_db`.`shop`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`shop` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`shop` (
  `shop_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `shop_name` VARCHAR(45) NOT NULL,
  `shop_location` VARCHAR(45) NOT NULL,
  `shop_coordinates` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`shop_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `delivery_app_db`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`category` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`category` (
  `category_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `delivery_app_db`.`order`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`order` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`order` (
  `order_id` INT UNSIGNED NOT NULL,
  `destination` VARCHAR(45) NOT NULL,
  `pickup_point` VARCHAR(45) NOT NULL,
  `orderedtime` DATETIME NOT NULL,
  `quantity` INT UNSIGNED NOT NULL,
  `rider_id` INT UNSIGNED NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `amountpaid` DECIMAL(15,2) NOT NULL,
  PRIMARY KEY (`order_id`),
  INDEX `fk_order_rider_personal1_idx` (`rider_id` ASC),
  INDEX `fk_order_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_order_rider_personal1`
    FOREIGN KEY (`rider_id`)
    REFERENCES `delivery_app_db`.`rider` (`rider_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `delivery_app_db`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `delivery_app_db`.`item`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`item` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`item` (
  `item_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `unit_price` DECIMAL(10,2) UNSIGNED NOT NULL,
  `item_name` VARCHAR(45) NOT NULL,
  `category_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`item_id`),
  INDEX `fk_item_category1_idx` (`category_id` ASC),
  CONSTRAINT `fk_item_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `delivery_app_db`.`category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'contains the individual items that shops can sell.\none item has only one category but one category has one or more items';


-- -----------------------------------------------------
-- Table `delivery_app_db`.`orderitem`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`orderitem` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`orderitem` (
  `order_id` INT UNSIGNED NOT NULL,
  `item_id` INT UNSIGNED NOT NULL,
  `item_quantity` INT NOT NULL,
  INDEX `fk_orderitem_order1_idx` (`order_id` ASC),
  INDEX `fk_orderitem_item1_idx` (`item_id` ASC),
  CONSTRAINT `fk_orderitem_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `delivery_app_db`.`order` (`order_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orderitem_item1`
    FOREIGN KEY (`item_id`)
    REFERENCES `delivery_app_db`.`item` (`item_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `delivery_app_db`.`shopcategory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`shopcategory` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`shopcategory` (
  `shop_shop_id` INT UNSIGNED NOT NULL,
  `category_category_id` INT UNSIGNED NOT NULL,
  INDEX `fk_shopcategory_shop1_idx` (`shop_shop_id` ASC),
  INDEX `fk_shopcategory_category1_idx` (`category_category_id` ASC),
  CONSTRAINT `fk_shopcategory_shop1`
    FOREIGN KEY (`shop_shop_id`)
    REFERENCES `delivery_app_db`.`shop` (`shop_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_shopcategory_category1`
    FOREIGN KEY (`category_category_id`)
    REFERENCES `delivery_app_db`.`category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `delivery_app_db`.`delivery`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `delivery_app_db`.`delivery` ;

CREATE TABLE IF NOT EXISTS `delivery_app_db`.`delivery` (
  `delivery_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `delivery_status` TINYINT(1) NOT NULL,
  `delivery_duration` TIME(0) NOT NULL,
  `order_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`delivery_id`),
  INDEX `fk_delivery_order1_idx` (`order_id` ASC),
  CONSTRAINT `fk_delivery_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `delivery_app_db`.`order` (`order_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'the status shows whether the trip was cancelled or not\nsay true for cancelled \n      false for not cancelled';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
