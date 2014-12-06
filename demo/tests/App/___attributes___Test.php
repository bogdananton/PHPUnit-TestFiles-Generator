<?php
namespace tests\\projects\PHPUnit-TestFiles-Generator\demo\source\App;

class ___attributes___ extends \PHPUnit_Framework_TestCase
{
   /**
	 * protected attribute Cart is defined
	 */
	public function testProtectedAttributeCartIsDefined()
	{
		$this->assertClassHasAttribute('Cart', '\App');
	}

	public function testIncomplete()
	{
		$this->markTestIncomplete(" ... ");
	}
}
