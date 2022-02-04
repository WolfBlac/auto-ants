
#include <tins/tcp_ip/stream_follower.h>
#include <tins/tins.h>

#include <spicy/rt/libspicy.h>

#include <codecvt>
#include <iostream>

std::ostream& operator<<( std::ostream& o, const std::u32string& s )
{
    std::wstring_convert< std::codecvt_utf8_utf16< char32_t >, char32_t > converter;
    std::cout << converter.to_bytes( s ) << std::endl;
    return o;
}

std::ostream& operator<<( std::ostream& o, const std::u16string& s )
{
    std::wstring_convert< std::codecvt_utf8_utf16< char16_t >, char16_t > converter;
    std::cout << converter.to_bytes( s ) << std::endl;
    return o;
}

void on_client_data( Tins::TCPIP::Stream& stream )
{
    const Tins::TCPIP::Stream::payload_type& s_payload = stream.server_payload();
    const Tins::TCPIP::Stream::payload_type& cl_payload = stream.client_payload();

    // std::string str( s_payload.begin(), s_payload.end() );
    // std::u32string cl_str( cl_payload.begin(), cl_payload.end() );
    // std::cout << "on_client_data:" << std::endl << str << std::endl; // << cl_str << std::endl;
}

void on_server_data( Tins::TCPIP::Stream& stream )
{
    const Tins::TCPIP::Stream::payload_type& s_payload = stream.server_payload();
    const Tins::TCPIP::Stream::payload_type& cl_payload = stream.client_payload();

    // std::u16string sstr( s_payload.begin(), s_payload.end() );
    // std::u16string cl_str( cl_payload.begin(), cl_payload.end() );
    // std::cout << "on_server_data:" << std::endl << sstr << std::endl << cl_str << std::endl;

    std::string str( s_payload.begin(), s_payload.end() );
    if ( str.find( "WallDurability" ) != std::string::npos ) {
        // std::u16string u16;
        // qi::parse( str.begin(), str.end(), *( "\\u" >> qi::hex ), u16 );
        // std::string u8
        //     = std::wstring_convert< std::codecvt_utf8_utf16< char16_t >, char16_t >().to_bytes(
        //         u16 );
        std::cout << "on_server_data: " << std::showbase << std::hex << str << std::endl;
        // print_characters( str.c_str() );
    }
}

void on_new_stream( Tins::TCPIP::Stream& stream )
{
    stream.auto_cleanup_payloads( true );
    // stream.ignore_client_data();

    std::cout << "on_new_stream" << std::endl;

    stream.client_data_callback( &on_client_data );
    stream.server_data_callback( &on_server_data );
}

void on_stream_terminated(
    Tins::TCPIP::Stream& stream, Tins::TCPIP::StreamFollower::TerminationReason reason )
{
    std::cout << "on_stream_terminated: " << reason << std::endl;
}

void process( Tins::Packet& packet )
{
    const auto& ts = packet.timestamp();
    std::cout << ts.seconds() << ":" << ts.microseconds() << std::endl;
}

int main()
{
    Tins::SnifferConfiguration config;
    config.set_promisc_mode( true );
    config.set_filter( "host 75.2.101.205 or host 99.83.178.222" );

    Tins::TCPIP::StreamFollower follower;
    follower.follow_partial_streams( true );
    follower.new_stream_callback( &on_new_stream );
    follower.stream_termination_callback( &on_stream_terminated );

    Tins::Sniffer sniffer( "en0", config );
    sniffer.sniff_loop( [&]( Tins::PDU& pdu ) {
        follower.process_packet( pdu );
        return true;
    } );
}
