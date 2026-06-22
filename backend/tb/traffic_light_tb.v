`timescale 1ns/1ps
module traffic_light_tb;
    reg clk = 0;
    reg reset = 1;
    reg ns_sensor = 0;
    reg ew_sensor = 0;
    reg pedestrian_request = 0;
    reg emergency = 0;
    reg night_mode = 0;

    wire ns_red, ns_yellow, ns_green;
    wire ew_red, ew_yellow, ew_green;
    wire ped_walk, ped_stop;

    traffic_light_controller DUT (
        .clk(clk), .reset(reset),
        .ns_sensor(ns_sensor), .ew_sensor(ew_sensor),
        .pedestrian_request(pedestrian_request),
        .emergency(emergency), .night_mode(night_mode),
        .ns_red(ns_red), .ns_yellow(ns_yellow), .ns_green(ns_green),
        .ew_red(ew_red), .ew_yellow(ew_yellow), .ew_green(ew_green),
        .ped_walk(ped_walk), .ped_stop(ped_stop)
    );

    always #5 clk = ~clk;

    always @(posedge clk) begin
        if (ns_green && ew_green) begin
            $display("ERROR: both NS and EW green are ON together");
            $finish;
        end
    end

    initial begin
        $dumpfile("traffic_light.vcd");
        $dumpvars(0, traffic_light_tb);
        $display("Starting FPGA Traffic Light Controller simulation");

        #20 reset = 0;
        #80 ew_sensor = 1;
        #80 ew_sensor = 0;
        #80 pedestrian_request = 1;
        #20 pedestrian_request = 0;
        #100 emergency = 1;
        #50 emergency = 0;
        #100 night_mode = 1;
        #80 night_mode = 0;
        #200;

        $display("Simulation completed successfully");
        $finish;
    end
endmodule
