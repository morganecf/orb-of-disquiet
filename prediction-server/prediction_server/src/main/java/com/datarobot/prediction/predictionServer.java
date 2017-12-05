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

import java.io.*;
import java.net.*;

import org.apache.commons.cli.Options;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;

/*
 * Launches Java server to serve predictions to clients sending strings.
 */

class PredictionServer {

    private final String STOP_CMD = "STOP";

    private ServerSocket server;
    private Socket client;
    private BufferedReader in;
    private PrintWriter out;
    private Predictor model;

    public PredictionServer(String jarPath, int port) {
        port = port;

        // Load model jar file
        URLClassLoader child;
        try {
            URL url = new File(jarPath).toURI().toURL();
            ClassLoader parent = PredictionServer.class.getClassLoader();
            child = new URLClassLoader(new URL[] { url }, parent);
        } catch (Exception e) {
            throw new RuntimeException("Unable to find jar path");
        }

        String packageName = Paths.get(jarPath).getFileName().toString().replace(".jar", "");

        // Load the model class
        Class modelClass;
        try {
            modelClass = Class.forName("com.datarobot.prediction.dr" + packageName + ".DRModel", true, child);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException("Unable to resolve classname automatically.");
        }

        // Initialize model for predictions
        try {
            model = (Predictor)modelClass.newInstance();
        } catch (Exception e) {
            throw new RuntimeException("Unable to create new model instance");
        }

        try {
            server = new ServerSocket(port);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void run() {
        String incoming;
        String outgoing;

        boolean running = true;

        try {
            // Blocked here until a client connects
            System.out.println("Waiting for connection...");
            client = server.accept();
            System.out.println("Received connection");

            // Listen for incoming messages
            while (running) {
                // To read from socket
                in = new BufferedReader(new InputStreamReader(client.getInputStream()));

                // To write to socket
                out = new PrintWriter(client.getOutputStream(), true);

                incoming = in.readLine();

                if (incoming.equals(STOP_CMD)) {
                    running = false;
                    break;
                }

                System.out.println("Predicting on:" + incoming);

                // Create record to score
                Row row = new Row();

                // Record has no numerical predictors and only one string predictor (text)
                row.d = new double[0];
                row.s = new String[1];
                row.s[0] = incoming;

                // Get score
                double score;
                try {
                    score = model.score(row);
                } catch (Exception e) {
                    throw new RuntimeException("Unable to score text");
                }

                String scoreStr = String.format("%.8f", score);

                out.println(scoreStr);
                System.out.println(scoreStr);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        this.stop();
    }

    public void stop() {
        System.out.println("Shutting down server");
        try {
            out.println("Connection closing");
            server.close();
        } catch (IOException e) {
            System.out.println("Error closing server connection.");
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws Exception {
        Options options = new Options();
        options.addOption("m", true, "model jar path (e.g. 587984b1100d2b625744477b.jar)");
        options.addOption("p", true, "port");

        try {
            CommandLineParser cliParser = new DefaultParser();
            CommandLine cmd = cliParser.parse(options, args);

            String jarPath = cmd.getOptionValue("m", "9000");
            int port = Integer.parseInt(cmd.getOptionValue("p"));

            PredictionServer server = new PredictionServer(jarPath, port);
            server.run();
        } catch (Exception e) {
            System.out.println(e.toString());
            // Generate help statement
            HelpFormatter formatter = new HelpFormatter();
            formatter.printHelp( "java -jar prediction_server.jar", options);
        }
    }
}
