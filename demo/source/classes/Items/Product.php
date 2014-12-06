<?php

class Product
{
	public $Code;
	public $Quantity;

	/**
	 * @todounit when passing an invalid data type for quantity then throw exception
	 */
	public function __construct($ProductCode = "", $Quantity = 1)
	{
		$this->Code = $ProductCode;
		$this->Quantity = (int)$Quantity;
	}
}
