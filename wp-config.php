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
define('AUTH_KEY',         ',^YJCe_yk|[,.Y5yw!O2p@;2)bk8*E;PCP$=H9`Jz!_eX+hbtF7BLdZE{Cfi}x(Y');
define('SECURE_AUTH_KEY',  'j}CZV6f~#kNC|{&+e0XiBOp|P9wA@-|Qa--A #45X~rtU6ucEC{+uc*Yd-4_W02)');
define('LOGGED_IN_KEY',    '8=@@4DkFi`L@=)Mq3RlVUy1=:M1ydH4E~/-TYG%?*$-@t=8~[zMhf6nR<.Xsg/vg');
define('NONCE_KEY',        'jJ@/yF^&X]okkqrIY+?muN(}^<,o-T(ibPa6})3T_}%o@)n55fi8_]*O zc{IGGJ');
define('AUTH_SALT',        ':t%(  -Ih`-B8d?D`Xjn#@K<<n@J?byKf-lsqj4Wt1K;fv|>ZTE5WaFwSa2 Jw~,');
define('SECURE_AUTH_SALT', 'XuL~-u0yD!DT|{|05i-=[[QJAywAkwqu`Bu)_Rm3D%8uhX>U.^dap:xq8Okj:YL+');
define('LOGGED_IN_SALT',   '=?*zB-2gXgnZ4 ei6LYP{yEYpLdi2z8nN[bReHJFLqRPC6YzLN`|7qtYa`7{jnx|');
define('NONCE_SALT',       'a++h|L_#0>DeKOW@8%Bl[-~*P&jxnH2PF7Qb[xs.RPi#8GpRBB4|i?s/NC-`^E9q');

define('FS_METHOD', 'direct');

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
