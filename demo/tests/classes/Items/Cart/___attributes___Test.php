<?php
namespace tests\classes\Items\Cart;

class ___attributes___ extends \PHPUnit_Framework_TestCase
{
   /**
     * static public attribute instance is defined
     */
    public function testStaticPublicAttributeInstanceIsDefined()
    {
        $this->assertClassHasStaticAttribute('instance', '\');
    }

   /**
     * public attribute Items is defined
     */
    public function testPublicAttributeItemsIsDefined()
    {
        $this->assertClassHasAttribute('Items', '\');
    }

   /**
     * public attribute Totals is defined
     */
    public function testPublicAttributeTotalsIsDefined()
    {
        $this->assertClassHasAttribute('Totals', '\');
    }

	public function testIncomplete()
	{
		$this->markTestIncomplete(" ... ");
	}
}
