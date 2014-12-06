<?php
namespace tests\\projects\PHPUnit-TestFiles-Generator\demo\source\classes\Totals\Obj\Totals;

class ___attributes___ extends \PHPUnit_Framework_TestCase
{
   /**
	 * public attribute Discount is defined
	 */
	public function testPublicAttributeDiscountIsDefined()
	{
		$this->assertClassHasAttribute('Discount', '\Totals');
	}

   /**
	 * public attribute GrossPrice is defined
	 */
	public function testPublicAttributeGrosspriceIsDefined()
	{
		$this->assertClassHasAttribute('GrossPrice', '\Totals');
	}

   /**
	 * public attribute NetPrice is defined
	 */
	public function testPublicAttributeNetpriceIsDefined()
	{
		$this->assertClassHasAttribute('NetPrice', '\Totals');
	}

   /**
	 * public attribute VAT is defined
	 */
	public function testPublicAttributeVatIsDefined()
	{
		$this->assertClassHasAttribute('VAT', '\Totals');
	}

	public function testIncomplete()
	{
		$this->markTestIncomplete(" ... ");
	}
}
