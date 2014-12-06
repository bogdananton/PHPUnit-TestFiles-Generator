<?php
namespace tests\\projects\PHPUnit-TestFiles-Generator\demo\source\classes\Items\Product;

class ___attributes___ extends \PHPUnit_Framework_TestCase
{
   /**
	 * public attribute Quantity is defined
	 */
	public function testPublicAttributeQuantityIsDefined()
	{
		$this->assertClassHasAttribute('Quantity', '\Product');
	}

   /**
	 * public attribute Code is defined
	 */
	public function testPublicAttributeCodeIsDefined()
	{
		$this->assertClassHasAttribute('Code', '\Product');
	}

	public function testIncomplete()
	{
		$this->markTestIncomplete(" ... ");
	}
}
