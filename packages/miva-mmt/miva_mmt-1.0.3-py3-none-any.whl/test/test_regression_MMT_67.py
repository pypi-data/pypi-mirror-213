from mmt.exceptions import Error
from test import MMTTest


class Test( MMTTest ):
	def test( self ):
		self.import_store_provisioning_file( 'regression_MMT-67.xml' )
		self.checkout()

		with self.template_open( 'regression_mmt-67.mvt', 'w' ) as fh:
			fh.write( 'The <mvt:item name="regression_MMT-67" /> references an invalid item and should error on compilation' )

		with self.assertRaises( Error ) as e:
			self.push( 'test_regression_MMT_67' )

		self.assertEqual( e.exception.error_message, 'Changeset_Create: One or more parameters are invalid: Template_Changes[1]: Error compiling template: regression_MMT-67 is not in the list of valid items' )
