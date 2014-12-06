<?php
namespace tests\classes\Totals\Obj\Totals;

class ___attributes___ extends \PHPUnit_Framework_TestCase
{
   /**
     * public attribute Discount is defined
     */
    public function testPublicAttributeDiscountIsDefined()
    {
        $this->assertClassHasAttribute('Discount', '\');
    }

   /**
     * public attribute GrossPrice is defined
     */
    public function testPublicAttributeGrosspriceIsDefined()
    {
        $this->assertClassHasAttribute('GrossPrice', '\');
    }

   /**
     * public attribute NetPrice is defined
     */
    public function testPublicAttributeNetpriceIsDefined()
    {
        $this->assertClassHasAttribute('NetPrice', '\');
    }

   /**
     * public attribute VAT is defined
     */
    public function testPublicAttributeVatIsDefined()
    {
        $this->assertClassHasAttribute('VAT', '\');
    }

	public function testIncomplete()
	{
		$this->markTestIncomplete(" ... ");
	}
}
