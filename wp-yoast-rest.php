<?php
/**
 * Exposes Yoast SEO meta fields to the WordPress REST API so the
 * publisher script can set SEO title / meta description / focus keyword.
 *
 * WITHOUT this, WordPress silently ignores those fields and you would
 * have to fill the Yoast box by hand on each post.
 *
 * INSTALL (pick one):
 *   A) Paste into your child theme's functions.php
 *   B) Better: install the "Code Snippets" plugin and add it there,
 *      so an Elementor/theme update can't wipe it.
 */

add_action( 'init', function () {

    $fields = array(
        '_yoast_wpseo_title',
        '_yoast_wpseo_metadesc',
        '_yoast_wpseo_focuskw',
    );

    foreach ( $fields as $field ) {
        foreach ( array( 'post', 'page' ) as $post_type ) {
            register_post_meta( $post_type, $field, array(
                'type'          => 'string',
                'single'        => true,
                'show_in_rest'  => true,
                'auth_callback' => function () {
                    return current_user_can( 'edit_posts' );
                },
            ) );
        }
    }
} );
