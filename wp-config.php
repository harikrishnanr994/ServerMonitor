<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //

define('DB_CHARSET', 'utf8');

define('DB_COLLATE', '');


define('DB_NAME', 'wordpress');
define('DB_USER', 'wordpressuser');
define('DB_PASSWORD', 'wordpress');
define('DB_HOST', 'localhost');
define('AUTH_KEY',         'k#m`9A*q,lG,8Wye{a7w307(L(rTjaO 6O>[HLUZf|-m61w&IK[)V-:9S^`9KJ*a');
define('SECURE_AUTH_KEY',  'ftzTMf9n(zv~B>I8Tr|Xh-GCi*T79q~@/-q:+@ Nji$KQXC=|Y5%w:1cI)tsQpba');
define('LOGGED_IN_KEY',    'iV*w#V:~ka0T2c1+f~jUoj{v:!=c Sq4:[+t`g]=5JJMycCQi+$H@ XNczAEnk4f');
define('NONCE_KEY',        '*j+2K35H~3`L gbo0|_5>YJrrnJg:*pQ nRGDL?KgB+:_H<NmsjT+qQU&+-[F^K[');
define('AUTH_SALT',        'piUFSp-I9BWkn :U5I^zoM,!rt;u?jj#h74-M20_,wJ>bt-Dvz2PW|}zOeWnn_PF');
define('SECURE_AUTH_SALT', 'P^`Pwa4NKl~r{{LQ?-`ia,A[5j,Ur^M_-;rT;C+m/L%#iA,k||j^@qgz6UxS:V.o');
define('LOGGED_IN_SALT',   'ynA+7>70Jt+oU3d|$Op^ZB2$b|l1%y,_=>7!|&*vu?epVmD?m>6KbVt`-Nl+I+$U');
define('NONCE_SALT',       'l{u{vFKck`P(5F. 1zrj}6Lk`-#+ik@FjniC=EG[<l+H69PfAooXcar?Id~z8]O(');

define('FS_METHOD', 'direct');
define('FORCE_SSL', true);
define('FORCE_SSL_ADMIN',true);
/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
