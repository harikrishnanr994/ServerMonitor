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
define('AUTH_KEY',         'uP|XFF=Gu6Iq-jZ=N,m?%@_|Ec-V? (bY6#B[#.y*@8(!+HW(]n/>JsYXQ>x}X}-');
define('SECURE_AUTH_KEY',  '!:VLoOFJUTe^elxt4V-nSp`f*}RQz!Ptxh~|w~|bO|cBxn:l88lg%PuC0.b%x(1_');
define('LOGGED_IN_KEY',    '0goD)AWM8J<%z8=R)g_HZGZl zr,{)g?F<@kY-Yzn|{z`Iy{*xL+!sx6*(*q!:+,');
define('NONCE_KEY',        't+PDU7Czx.g@!C+CZz_kufK6d@y1-7DD^}dh0c#r3enp)p]sAfPdLs-c>At~!IQv');
define('AUTH_SALT',        'dQ]a6C^?)]-5IIb=rVCp(^{hwd73YiJ8G,/n+ox,Q{_9{!_8wy^lQH~fO8?^X?;m');
define('SECURE_AUTH_SALT', 'P1h4e;Vrz,o=kCna*c3M[[C-J%6R5|F<_Hw{IswG>&<I(.8{ u6TVhCgh#1 hu.X');
define('LOGGED_IN_SALT',   'xx)m6<y`9:Z8Op&`dZ2Yvz-)CR?%e|zw))Jl9<1iwZ/^}lhCQz0nG-4u7s18R{md');
define('NONCE_SALT',       'bkKrYmJV6()A=ypXZ7lO!8oD<=|)Z#a>dg$c9C|s8 <+h NqoOmj(QRl#=#^YM^X');

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
