#include <stdio.h>
#include <stdlib.h>

#include <iostream>
#include <string>

#include <pybind11/pybind11.h>
#include <windivert.h>

namespace py = pybind11;

#define ntohs(x) WinDivertHelperNtohs(x)
#define ntohl(x) WinDivertHelperNtohl(x)
#define htons(x) WinDivertHelperHtons(x)
#define htonl(x) WinDivertHelperHtonl(x)

#define MAXBUF WINDIVERT_MTU_MAX

HANDLE handle = INVALID_HANDLE_VALUE;

UINT32 g_clientIpBuf[4];
std::string g_filter;

void init(std::string filter, std::string localIp)
{
    g_filter = filter;

    printf("Using filter \"%s\"\n", g_filter.c_str());

    handle = WinDivertOpen(g_filter.c_str(), WINDIVERT_LAYER_NETWORK, 0, 0);
    if (handle == INVALID_HANDLE_VALUE)
    {
        auto err = GetLastError();
        fprintf(stderr, "error: failed to open the WinDivert device (%d)\n", err);
        if (err == 5)
            fprintf(stderr, "The calling application does not have Administrator privileges.\n");
        exit(EXIT_FAILURE);
    }

    if (!WinDivertHelperParseIPv4Address(localIp.c_str(), g_clientIpBuf))
    {
        std::cerr << "WinDivertHelperFormatIPv4Address SrcAddr failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    printf("WinDivert initialized\n");
}

void inj(std::string pkt)
{
    char *packet = &pkt[0];
    WINDIVERT_ADDRESS addr;
    UINT packet_len = (UINT)pkt.length();
    PWINDIVERT_IPHDR ip_header;

    if (!WinDivertHelperParsePacket(packet, packet_len, &ip_header, NULL,
                                    NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                                    NULL, NULL))
    {
        std::cerr << "WinDivertHelperParsePacket failed" << std::endl;
        return;
    }

    ip_header->DstAddr = htonl(*g_clientIpBuf);

    addr.Outbound = 1;

    if (!WinDivertHelperCalcChecksums((PVOID)packet, packet_len, &addr, 0))
    {
        std::cerr << "WinDivertHelperCalcChecksums failed" << std::endl;
        return;
    }

    py::gil_scoped_release release;

    if (!WinDivertSend(handle, packet, packet_len, NULL, &addr))
    {
        std::cerr << "WinDivertSend failed" << std::endl;
        return;
    }

    py::gil_scoped_acquire acquire;
}

py::bytes get()
{
    WINDIVERT_ADDRESS addr;
    char packet[MAXBUF];
    UINT packet_len;

    py::gil_scoped_release release;

    if (!WinDivertRecv(handle, packet, sizeof(packet), &packet_len, &addr))
    {
        fprintf(stderr, "warning: failed to read packet (%d)\n",
                GetLastError());
    }

    py::gil_scoped_acquire acquire;

    // if (!WinDivertHelperParsePacket(packet, packet_len, NULL, NULL,
    //                                 NULL, NULL, NULL, NULL, NULL, NULL, NULL,
    //                                 NULL, NULL))
    // {
    //     std::cerr << "WinDivertHelperParsePacket failed" << std::endl;
    // }

    // if (!WinDivertHelperCalcChecksums((PVOID)packet, packet_len, &addr, 0))
    // {
    //     std::cerr << "WinDivertHelperCalcChecksums failed" << std::endl;
    // }

    return py::bytes(packet, packet_len);
}

void stop()
{
    if (handle != INVALID_HANDLE_VALUE)
    {
        if (!WinDivertClose(handle))
        {
            fprintf(stderr, "error: failed to close the WinDivert device (%d)\n",
                    GetLastError());
        }
    }
    handle = INVALID_HANDLE_VALUE;
}

PYBIND11_MODULE(_toori, m)
{
    m.def("init", &init);

    m.def("get", &get);

    m.def("inj", &inj);

    m.def("stop", &stop);
}
