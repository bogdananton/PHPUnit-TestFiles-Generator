<?php
namespace tests\classes\Items\Product;

class ___attributes___ extends \PHPUnit_Framework_TestCase
{
   /**
     * public attribute Quantity is defined
     */
    public function testPublicAttributeQuantityIsDefined()
    {
        $this->assertClassHasAttribute('Quantity', '\');
    }

   /**
     * public attribute Code is defined
     */
    public function testPublicAttributeCodeIsDefined()
    {
        $this->assertClassHasAttribute('Code', '\');
    }

	public function testIncomplete()
	{
		$this->markTestIncomplete(" ... ");
	}
}
