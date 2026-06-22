`timescale 1ns/1ps
// FPGA-Based Traffic Light Controller RTL
// States: NS_GREEN, NS_YELLOW, ALL_RED_1, EW_GREEN, EW_YELLOW, ALL_RED_2,
// PED_WALK, EMERGENCY_ALL_RED, NIGHT_BLINK

module traffic_light_controller #(
    parameter GREEN_TIME  = 5,
    parameter YELLOW_TIME = 2,
    parameter ALL_RED_TIME = 1,
    parameter WALK_TIME = 4
)(
    input  wire clk,
    input  wire reset,
    input  wire ns_sensor,
    input  wire ew_sensor,
    input  wire pedestrian_request,
    input  wire emergency,
    input  wire night_mode,
    output reg  ns_red,
    output reg  ns_yellow,
    output reg  ns_green,
    output reg  ew_red,
    output reg  ew_yellow,
    output reg  ew_green,
    output reg  ped_walk,
    output reg  ped_stop
);

    localparam NS_GREEN          = 4'd0;
    localparam NS_YELLOW         = 4'd1;
    localparam ALL_RED_1         = 4'd2;
    localparam EW_GREEN          = 4'd3;
    localparam EW_YELLOW         = 4'd4;
    localparam ALL_RED_2         = 4'd5;
    localparam PED_WALK_STATE    = 4'd6;
    localparam EMERGENCY_ALL_RED = 4'd7;
    localparam NIGHT_BLINK       = 4'd8;

    reg [3:0] state;
    reg [3:0] next_state;
    reg [7:0] timer;
    reg ped_latched;
    reg blink;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            state <= NS_GREEN;
            timer <= 0;
            ped_latched <= 0;
            blink <= 0;
        end else begin
            if (pedestrian_request)
                ped_latched <= 1'b1;
            if (state == PED_WALK_STATE && timer >= WALK_TIME)
                ped_latched <= 1'b0;

            blink <= ~blink;

            if (emergency) begin
                state <= EMERGENCY_ALL_RED;
                timer <= 0;
            end else if (night_mode) begin
                state <= NIGHT_BLINK;
                timer <= 0;
            end else begin
                state <= next_state;
                if (next_state != state)
                    timer <= 0;
                else
                    timer <= timer + 1'b1;
            end
        end
    end

    always @(*) begin
        next_state = state;
        case (state)
            NS_GREEN: begin
                if (timer >= GREEN_TIME && (ew_sensor || ped_latched))
                    next_state = NS_YELLOW;
            end
            NS_YELLOW: begin
                if (timer >= YELLOW_TIME)
                    next_state = ALL_RED_1;
            end
            ALL_RED_1: begin
                if (timer >= ALL_RED_TIME)
                    next_state = ped_latched ? PED_WALK_STATE : EW_GREEN;
            end
            EW_GREEN: begin
                if (timer >= GREEN_TIME && (ns_sensor || ped_latched))
                    next_state = EW_YELLOW;
            end
            EW_YELLOW: begin
                if (timer >= YELLOW_TIME)
                    next_state = ALL_RED_2;
            end
            ALL_RED_2: begin
                if (timer >= ALL_RED_TIME)
                    next_state = ped_latched ? PED_WALK_STATE : NS_GREEN;
            end
            PED_WALK_STATE: begin
                if (timer >= WALK_TIME)
                    next_state = NS_GREEN;
            end
            EMERGENCY_ALL_RED: begin
                if (!emergency)
                    next_state = NS_GREEN;
            end
            NIGHT_BLINK: begin
                if (!night_mode)
                    next_state = NS_GREEN;
            end
            default: next_state = NS_GREEN;
        endcase
    end

    always @(*) begin
        ns_red = 0; ns_yellow = 0; ns_green = 0;
        ew_red = 0; ew_yellow = 0; ew_green = 0;
        ped_walk = 0; ped_stop = 1;

        case (state)
            NS_GREEN: begin
                ns_green = 1; ew_red = 1; ped_stop = 1;
            end
            NS_YELLOW: begin
                ns_yellow = 1; ew_red = 1; ped_stop = 1;
            end
            ALL_RED_1, ALL_RED_2: begin
                ns_red = 1; ew_red = 1; ped_stop = 1;
            end
            EW_GREEN: begin
                ns_red = 1; ew_green = 1; ped_stop = 1;
            end
            EW_YELLOW: begin
                ns_red = 1; ew_yellow = 1; ped_stop = 1;
            end
            PED_WALK_STATE: begin
                ns_red = 1; ew_red = 1; ped_walk = 1; ped_stop = 0;
            end
            EMERGENCY_ALL_RED: begin
                ns_red = 1; ew_red = 1; ped_stop = 1;
            end
            NIGHT_BLINK: begin
                ns_yellow = blink;
                ew_red = blink;
                ped_stop = 1;
            end
            default: begin
                ns_red = 1; ew_red = 1; ped_stop = 1;
            end
        endcase
    end
endmodule
