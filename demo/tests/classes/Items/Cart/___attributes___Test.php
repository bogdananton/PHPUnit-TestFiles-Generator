<?php
namespace tests\\projects\PHPUnit-TestFiles-Generator\demo\source\classes\Items\Cart;

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
		$this->assertClassHasAttribute('Items', '\Cart');
	}

   /**
	 * public attribute Totals is defined
	 */
	public function testPublicAttributeTotalsIsDefined()
	{
		$this->assertClassHasAttribute('Totals', '\Cart');
	}

	public function testIncomplete()
	{
		$this->markTestIncomplete(" ... ");
	}
}
