package com.datarobot.prediction;

import com.datarobot.prediction.Predictor;
import com.datarobot.prediction.Row;
import com.datarobot.transform.util.InputUtils;

import java.net.URL;
import java.net.URLClassLoader;
import java.io.File;
import java.nio.file.Paths;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Map;
import java.util.HashMap;

import org.apache.commons.cli.Options;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;

class RowTester {

    private static void makePredictions(String jarPath, String modelId, String inputRow) throws Exception {

        // load jar file
        URLClassLoader child = new URLClassLoader(
            new URL[] {new File(jarPath).toURI().toURL()},
            RowTester.class.getClassLoader());

        // load DRModel class
        String packageName = modelId != null ? modelId : Paths.get(jarPath).getFileName().toString().replace(".jar", "");
        Class drModelClass = null;
        try {
            drModelClass = Class.forName(
                "com.datarobot.prediction.dr" + packageName + ".DRModel", true, child);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException("Unable to resolve classname automatically. " +
                                "Please specify the model name (-l)");
        }

        // initialize model
        Predictor drModel = (Predictor)drModelClass.newInstance();

        // to read in user input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        System.out.println("Type something");

        // start reading in lines
        while (true) {
            // get input
            String text = br.readLine();

            // create record to score
            Row row = new Row();

            // record has no numerical predictors and only one string predictor (text)
            row.d = new double[0];
            row.s = new String[1];
            row.s[0] = text;

            // get score
            double score = drModel.score(row);

            System.out.println(String.format("%.8f", score));
        }
    }

    public static void main(String[] args) throws Exception {

        Options options = new Options();
        options.addOption("m", true, "model jar path (e.g. 587984b1100d2b625744477b.jar)");
        options.addOption("l", true, "model name (e.g. 587984b1100d2b625744477b)");
        options.addOption("s", true, "input row");

        try {
            // parse argumenrs
            CommandLineParser cliParser = new DefaultParser();
            CommandLine cmd = cliParser.parse(options, args);
            String jarPath = cmd.getOptionValue("m");
            String modelId = cmd.getOptionValue("l");
            String inputRow = cmd.getOptionValue("s");
            makePredictions(jarPath, modelId, inputRow);
        } catch (Exception e) {
            System.out.println(e.toString());
            // Generate help statement
            HelpFormatter formatter = new HelpFormatter();
            formatter.printHelp( "java -jar codegen_score_row.jar", options);
        }
    }

}
