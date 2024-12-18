import esbuild from 'esbuild';
import { sassPlugin } from 'esbuild-sass-plugin';
import fs from 'fs';

const isProduction = process.env.ENVIRONMENT === 'production';

const build = async (shouldWatch) => {
    const buildOptions = {
        plugins: [
            sassPlugin({
                quietDeps: true,
            }),
        ],
        entryPoints: [
            'app/static/src/js/app-bundle.js',
            'app/static/src/scss/styles.scss',
        ],
        bundle: true,
        entryNames: '[name]-[hash].min', // Output filenames with hashed names
        outdir: 'app/static/dist', // Output directory
        format: 'esm', // Outputs as ES Module
        minify: true, // Minify JS and CSS
        sourcemap: true, // Generates source maps
        external: ['/assets/*'], // External paths
        logLevel: 'info', // Logging level
        metafile: true, // Enables output metadata
    };

    try {
        const result = await esbuild.build(buildOptions);

        // Generate manifest.json mapping original names to hashed names
        const manifest = {};
        for (const [outputPath, outputInfo] of Object.entries(result.metafile.outputs)) {
            const fileName = outputPath.split('/').pop();
            if (outputInfo.entryPoint) {
                const originalName = outputInfo.entryPoint.split('/').pop();
                manifest[originalName] = fileName;
            }
        }

        // Write the manifest.json to the output directory
        fs.writeFileSync('app/static/dist/manifest.json', JSON.stringify(manifest, null, 2));
        console.log('Manifest generated:', manifest);

    } catch (error) {
        console.error('Build failed:', error);
        process.exit(1); // Exit with failure code
    }
};

const shouldWatch = process.argv.includes('--watch');
build(shouldWatch);
