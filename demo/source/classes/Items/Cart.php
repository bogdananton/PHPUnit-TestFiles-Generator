<?php

class Cart
{
	public $Totals = 0;
	public $Items;
	public static $instance;

	public function __construct()
	{
		$this->Items = array();
	}

	/**
	 * @todounit when passing a non-string as the product code then don't add the item
	 * @todounit if quantity is lower than 1 then don't add the item
	 * 
	 * @param string  $ProductCode
	 * @param integer $Quantity
	 */
	public function addItem($ProductCode = "", $Quantity = 1)
	{
		$this->Items[] = new Product($ProductCode, $Quantity);
		$this->refreshTotals();
	}

	public function debug($output = "HTML")
	{
		$this->test();
		print_r($this);
	}

	public function refreshTotals()
	{
		$this->Totals = 100 * count($this->Items);
	}
}
