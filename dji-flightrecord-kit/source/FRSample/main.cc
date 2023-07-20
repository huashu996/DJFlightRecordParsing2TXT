//
//  main.c
//  FlightRecordConversionServiceExecutable
//
//

#include <stdio.h>
#include "DJIFRProtoParser.hpp"
#include <assert.h>
#include <thread>
#include <unistd.h>
#include <google/protobuf/util/json_util.h>
#include <iostream>
#include <fstream>
#include <string>


int main(int argc, char *argv[]) {
    std::string file_path(argv[1]);
    auto parser = std::make_shared<DJIFRProto::Standard::Parser>();
    auto result = parser->load(file_path);
    if (result != DJIFRProto::Standard::Success) {
        printf("load file failed");
        return 0;
    }
    

    result = parser->startRequestParser(getenv("SDK_KEY"), [&parser](DJIFR::standardization::ServerError error_code, const std::string& error_description) {

        if (error_code == DJIFR::standardization::ServerError::Success) {
            std::shared_ptr<DJIFRProto::Standard::SummaryInformation> info = nullptr;
            parser->summaryInformation(&info);

            std::string summary_proto_json_string = "";
            std::string info_proto_json_string = "";

            google::protobuf::util::JsonPrintOptions options;
            options.add_whitespace = true;
            options.always_print_primitive_fields = true;
            options.preserve_proto_field_names = true;

            if (!google::protobuf::util::MessageToJsonString(*info, &summary_proto_json_string, options).ok()) {
                summary_proto_json_string = "{}";
            }

            std::shared_ptr<DJIFRProto::Standard::FrameTimeStates> frame_time_list;
            parser->frame_time_states(&frame_time_list);
            if (!google::protobuf::util::MessageToJsonString(*frame_time_list, &info_proto_json_string, options).ok()) {
                info_proto_json_string = "{}";
            }
            //printf("{\"summary\": %s, \"info\": %s}", summary_proto_json_string.c_str(), info_proto_json_string.c_str());
			 // 修改部分：使用文件输出流代替标准输出
			         // 新增部分：打开输出文件流
			std::ofstream output_file("/home/cxl/FlightRecordParsingLib-master/output.txt");
			if (!output_file) {
				std::cerr << "Error opening the output file." << std::endl;
				return 1;
			}
        	output_file << "{\"summary\": " << summary_proto_json_string << ", \"info\": " << info_proto_json_string << "}";
            output_file.close();     

        } else {
            //printf("error code: %d decription: %s\n", (int)error_code, error_description.c_str());
            // 修改部分：使用文件输出流代替标准输出
            // 新增部分：打开输出文件流
			std::ofstream output_file("/home/cxl/FlightRecordParsingLib-master/output.txt");
			if (!output_file) {
				std::cerr << "Error opening the output file." << std::endl;
				return 1;
			}
        	output_file << "error code: " << static_cast<int>(error_code) << " description: " << error_description;
        	output_file.close();     
        }
        // 新增部分：关闭输出文件流
    });
    return 0;
}
