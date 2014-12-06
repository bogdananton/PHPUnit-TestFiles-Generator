<?php
namespace tests\App;

class ___attributes___ extends \PHPUnit_Framework_TestCase
{
   /**
     * protected attribute Cart is defined
     */
    public function testProtectedAttributeCartIsDefined()
    {
        $this->assertClassHasAttribute('Cart', '\');
    }

	public function testIncomplete()
	{
		$this->markTestIncomplete(" ... ");
	}
}
